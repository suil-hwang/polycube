import pyvista as pv
import numpy as np
from typing import List, Union, Optional

def polycube_to_vtk(coords: List[List[Union[int, float]]], 
                   scale: float = 12.0,
                   smooth: bool = False) -> pv.PolyData:
    """
    폴리큐브 좌표를 VTK 메시로 변환합니다.
    
    Parameters:
    -----------
    coords : List[List[Union[int, float]]]
        폴리큐브 좌표 리스트
    scale : float
        큐브 크기 스케일
    smooth : bool
        모서리 스무딩 여부
        
    Returns:
    --------
    pv.PolyData
        VTK 폴리데이터 메시
    """
    if not coords:
        raise ValueError("좌표 리스트가 비어있습니다.")
    
    # 각 큐브 생성
    meshes = []
    for i, coord in enumerate(coords):
        center = [coord[0] * scale, coord[1] * scale, coord[2] * scale]
        
        if smooth:
            # 둥근 모서리를 위한 작은 큐브
            cube = pv.Cube(center=center, 
                          x_length=scale * 0.9, 
                          y_length=scale * 0.9, 
                          z_length=scale * 0.9)
            # 스무딩 적용
            cube = cube.subdivide(1).smooth(n_iter=10)
        else:
            # 일반 큐브
            cube = pv.Cube(center=center,
                          x_length=scale,
                          y_length=scale,
                          z_length=scale)
        
        meshes.append(cube)
    
    # 모든 큐브 병합
    print(f"병합 중: {len(meshes)} cubes")
    combined = meshes[0]
    for mesh in meshes[1:]:
        combined = combined.merge(mesh)
    
    # 중복 점 제거 및 최적화
    combined = combined.clean()
    
    return combined

def save_vtk(coords: List[List[Union[int, float]]], 
            filename: str, 
            scale: float = 12.0,
            smooth: bool = False):
    """
    폴리큐브를 VTK 파일로 저장합니다.
    
    Parameters:
    -----------
    coords : List[List[Union[int, float]]]
        폴리큐브 좌표
    filename : str
        출력 파일명 (확장자 제외)
    scale : float
        큐브 크기
    smooth : bool
        모서리 스무딩 여부
    """
    mesh = polycube_to_vtk(coords, scale, smooth)
    output_path = f"{filename}.vtk"
    mesh.save(output_path)
    print(f"VTK 파일 저장: {output_path}")

def save_vtu(coords: List[List[Union[int, float]]], 
            filename: str, 
            scale: float = 12.0,
            smooth: bool = False):
    """
    폴리큐브를 VTU 파일로 저장합니다.
    
    Parameters:
    -----------
    coords : List[List[Union[int, float]]]
        폴리큐브 좌표
    filename : str
        출력 파일명 (확장자 제외)
    scale : float
        큐브 크기
    smooth : bool
        모서리 스무딩 여부
    """
    mesh = polycube_to_vtk(coords, scale, smooth)
    output_path = f"{filename}.vtu"
    mesh.save(output_path)
    print(f"VTU 파일 저장: {output_path}")

def save_with_metadata(coords: List[List[Union[int, float]]],
                      filename: str,
                      scale: float = 12.0,
                      format: str = 'vtk',
                      metadata: Optional[dict] = None):
    """
    메타데이터와 함께 폴리큐브를 저장합니다.
    
    Parameters:
    -----------
    coords : List[List[Union[int, float]]]
        폴리큐브 좌표
    filename : str
        출력 파일명
    scale : float
        큐브 크기
    format : str
        파일 형식 ('vtk' 또는 'vtu')
    metadata : dict
        추가 메타데이터
    """
    mesh = polycube_to_vtk(coords, scale)
    
    # 메타데이터 추가
    if metadata:
        for key, value in metadata.items():
            mesh.field_data[key] = np.array([value])
    
    # 큐브 인덱스 추가
    mesh['cube_index'] = np.arange(len(coords))
    
    # 저장
    if format == 'vtk':
        mesh.save(f"{filename}.vtk")
    elif format == 'vtu':
        mesh.save(f"{filename}.vtu")
    else:
        raise ValueError(f"지원하지 않는 형식: {format}")