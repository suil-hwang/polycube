import trimesh
import numpy as np
from typing import List, Tuple, Union

def load_mesh(filepath: str) -> trimesh.Trimesh:
    """
    STL 또는 OBJ 파일을 로드합니다.
    
    Parameters:
    -----------
    filepath : str
        메시 파일 경로 (.stl, .obj 지원)
        
    Returns:
    --------
    trimesh.Trimesh
        로드된 메시 객체
    """
    try:
        mesh = trimesh.load(filepath, force='mesh')
        print(f"메시 로드 완료: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
        return mesh
    except Exception as e:
        raise ValueError(f"메시 파일을 로드할 수 없습니다: {e}")

def mesh_to_voxels(mesh: trimesh.Trimesh, pitch: float = 1.0) -> trimesh.voxel.VoxelGrid:
    """
    메시를 복셀 그리드로 변환합니다.
    
    Parameters:
    -----------
    mesh : trimesh.Trimesh
        입력 메시
    pitch : float
        복셀 크기 (기본값: 1.0)
        
    Returns:
    --------
    trimesh.voxel.VoxelGrid
        복셀 그리드
    """
    # 메시 경계 확인
    bounds = mesh.bounds
    print(f"메시 경계: {bounds}")
    
    # 복셀화
    voxels = mesh.voxelized(pitch=pitch)
    print(f"복셀 그리드 크기: {voxels.shape}")
    
    return voxels

def voxels_to_polycube_coords(voxels: trimesh.voxel.VoxelGrid) -> List[List[int]]:
    """
    복셀 그리드를 폴리큐브 좌표로 변환합니다.
    
    Parameters:
    -----------
    voxels : trimesh.voxel.VoxelGrid
        복셀 그리드
        
    Returns:
    --------
    List[List[int]]
        폴리큐브 좌표 리스트
    """
    # 채워진 복셀의 좌표 추출
    filled = voxels.matrix
    coords = np.argwhere(filled)
    
    # 좌표를 원점 기준으로 조정
    if len(coords) > 0:
        min_coords = coords.min(axis=0)
        coords = coords - min_coords
    
    return coords.tolist()

def mesh_to_polycube(filepath: str, voxel_size: float = 1.0, 
                    simplify: bool = True, max_cubes: int = 1000) -> List[List[int]]:
    """
    메시 파일을 폴리큐브 좌표로 변환합니다.
    
    Parameters:
    -----------
    filepath : str
        입력 메시 파일 경로
    voxel_size : float
        복셀 크기 (작을수록 세밀함)
    simplify : bool
        메시 단순화 여부
    max_cubes : int
        최대 큐브 개수 제한
        
    Returns:
    --------
    List[List[int]]
        폴리큐브 좌표 리스트
    """
    mesh = load_mesh(filepath)
    
    # 메시 단순화 (옵션)
    if simplify and len(mesh.faces) > 10000:
        target_faces = min(10000, len(mesh.faces))
        mesh = mesh.simplify_quadric_decimation(target_faces)
        print(f"메시 단순화: {target_faces} faces")
    
    # 복셀화
    voxels = mesh_to_voxels(mesh, pitch=voxel_size)
    coords = voxels_to_polycube_coords(voxels)
    
    # 큐브 개수 제한
    if len(coords) > max_cubes:
        print(f"경고: 큐브 개수({len(coords)})가 제한({max_cubes})을 초과합니다.")
        # 랜덤 샘플링으로 줄이기
        indices = np.random.choice(len(coords), max_cubes, replace=False)
        coords = [coords[i] for i in indices]
    
    print(f"생성된 폴리큐브: {len(coords)} cubes")
    return coords