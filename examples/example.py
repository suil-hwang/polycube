#!/usr/bin/env python3
"""
Bunny 모델을 폴리큐브로 변환하고 시각화하는 예제
모델 크기에 따라 자동으로 복셀 크기 조정
"""

import os
import trimesh
import numpy as np
from polycube import mesh_to_polycube, save_vtk, polycube_to_vtk, load_mesh
import pyvista as pv

def calculate_adaptive_voxel_size(mesh, target_cubes=500, min_resolution=20):
    """
    모델 크기에 따라 적절한 복셀 크기를 계산
    
    Parameters:
    -----------
    mesh : trimesh.Trimesh
        입력 메시
    target_cubes : int
        목표 큐브 개수 (대략적)
    min_resolution : int
        각 축의 최소 해상도
        
    Returns:
    --------
    float
        계산된 복셀 크기
    """
    # 메시의 경계 상자 크기 계산
    bounds = mesh.bounds
    dimensions = bounds[1] - bounds[0]
    
    # 가장 긴 축의 길이
    max_dimension = np.max(dimensions)
    
    # 각 축의 평균 길이
    avg_dimension = np.mean(dimensions)
    
    # 목표 큐브 개수를 달성하기 위한 복셀 크기 계산
    # 큐브 개수 ≈ (volume / voxel_size^3)
    volume = np.prod(dimensions)
    voxel_size_by_target = (volume / target_cubes) ** (1/3)
    
    # 최소 해상도를 보장하는 복셀 크기
    voxel_size_by_resolution = max_dimension / min_resolution
    
    # 두 값 중 작은 값 선택 (더 세밀한 복셀)
    voxel_size = min(voxel_size_by_target, voxel_size_by_resolution)
    
    # 너무 작은 복셀 크기 방지
    min_voxel_size = max_dimension / 100  # 최대 100x100x100 해상도
    voxel_size = max(voxel_size, min_voxel_size)
    
    print(f"\n모델 정보:")
    print(f"  - 경계 크기: {dimensions}")
    print(f"  - 최대 치수: {max_dimension:.4f}")
    print(f"  - 부피: {volume:.6f}")
    print(f"  - 계산된 복셀 크기: {voxel_size:.6f}")
    print(f"  - 예상 큐브 개수: {int(volume / (voxel_size**3))}\n")
    
    return voxel_size

def main():
    # 파일 경로
    input_file = os.path.join(os.path.dirname(__file__), 'bunny.obj')
    
    # 1. 먼저 메시를 로드하여 크기 확인
    print("메시 분석 중...")
    mesh = load_mesh(input_file)
    
    # 2. 적응적 복셀 크기 계산
    voxel_size = calculate_adaptive_voxel_size(
        mesh, 
        target_cubes=5000,  # 원하는 대략적인 큐브 개수
        min_resolution=20  # 각 축의 최소 해상도
    )
    
    # 3. 메시를 폴리큐브로 변환
    print("폴리큐브로 변환 중...")
    coords = mesh_to_polycube(
        input_file,
        voxel_size=voxel_size,
        max_cubes=5000  # 최대 큐브 개수 (메모리 보호)
    )
    print(f"생성된 큐브 개수: {len(coords)}")
    
    # 큐브가 너무 적으면 경고
    if len(coords) < 10:
        print("\n경고: 생성된 큐브가 너무 적습니다!")
        print("복셀 크기를 더 작게 조정합니다...")
        voxel_size = voxel_size / 2
        coords = mesh_to_polycube(input_file, voxel_size=voxel_size, max_cubes=1000)
        print(f"재조정 후 큐브 개수: {len(coords)}")
    
    # 4. 큐브 크기도 모델에 맞게 조정
    model_size = np.max(mesh.bounds[1] - mesh.bounds[0])
    cube_scale = model_size * 50  # 시각화를 위해 적절히 확대
    
    # 5. VTK 파일로 저장
    print(f"\nVTK 파일 저장 중...")
    save_vtk(coords, 'examples/bunny_polycube', scale=cube_scale)
    print("저장 완료: bunny_polycube.vtk")
    
    # 6. PyVista로 결과물 렌더링
    print("\n폴리큐브 시각화...")
    
    # 원본 메시와 폴리큐브 메시 생성
    polycube_mesh = polycube_to_vtk(coords, scale=cube_scale)
    
    # 원본 메시 스케일 조정 (비교를 위해)
    original_mesh = pv.wrap(mesh)
    center = original_mesh.center
    original_mesh.points = (original_mesh.points - center) * cube_scale / voxel_size + center
    
    # 시각화
    plotter = pv.Plotter(shape=(1, 2))
    
    # 왼쪽: 원본 메시
    plotter.subplot(0, 0)
    plotter.add_mesh(
        original_mesh,
        color='gray',
        opacity=0.5,
        show_edges=False
    )
    plotter.add_text("Original Mesh", position='upper_left')
    
    # 오른쪽: 폴리큐브
    plotter.subplot(0, 1)
    plotter.add_mesh(
        polycube_mesh, 
        color='lightblue',
        edge_color='black',
        show_edges=True,
        opacity=0.9
    )
    plotter.add_text(
        f"Polycube ({len(coords)} cubes)", 
        position='upper_left'
    )
    
    # 두 서브플롯 모두에 그리드와 축 추가
    plotter.subplot(0, 0)
    plotter.show_grid()
    plotter.add_axes()
    
    plotter.subplot(0, 1)
    plotter.show_grid()
    plotter.add_axes()
    
    # 카메라 링크 (두 뷰 동기화)
    plotter.link_views()
    
    # 렌더링
    plotter.show()

if __name__ == "__main__":
    main()

# python examples/example.py