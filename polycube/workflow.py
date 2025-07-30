from typing import List, Optional, Union
from .mesh_input import mesh_to_polycube
from .vtk_output import save_vtk, save_vtu, save_with_metadata
from .polycube import polycube
from .stl import scad_to_stl
from solid import scad_render_to_file

def convert_mesh_to_vtk(input_file: str, 
                       output_file: str, 
                       voxel_size: float = 1.0, 
                       scale: float = 12.0, 
                       format: str = 'vtk',
                       smooth: bool = False,
                       max_cubes: int = 1000) -> List[List[int]]:
    """
    메시 파일을 폴리큐브 VTK/VTU로 변환합니다.
    
    Parameters:
    -----------
    input_file : str
        입력 STL/OBJ 파일 경로
    output_file : str
        출력 파일명 (확장자 제외)
    voxel_size : float
        복셀화 크기
    scale : float
        큐브 크기
    format : str
        출력 형식 ('vtk' 또는 'vtu')
    smooth : bool
        모서리 스무딩 여부
    max_cubes : int
        최대 큐브 개수
        
    Returns:
    --------
    List[List[int]]
        생성된 폴리큐브 좌표
    """
    print(f"변환 시작: {input_file} -> {output_file}.{format}")
    
    # 메시를 폴리큐브 좌표로 변환
    coords = mesh_to_polycube(input_file, voxel_size, max_cubes=max_cubes)
    
    # 메타데이터 생성
    metadata = {
        'source_file': input_file,
        'voxel_size': voxel_size,
        'cube_count': len(coords),
        'scale': scale
    }
    
    # VTK/VTU로 저장
    save_with_metadata(coords, output_file, scale, format, metadata)
    
    print(f"변환 완료: {len(coords)} cubes")
    return coords

def convert_mesh_to_polycube_vtk(input_file: str,
                                output_base: str,
                                voxel_size: float = 1.0,
                                scale: float = 12.0,
                                generate_all: bool = True) -> List[List[int]]:
    """
    메시를 폴리큐브로 변환하고 여러 형식으로 출력합니다.
    
    Parameters:
    -----------
    input_file : str
        입력 메시 파일
    output_base : str
        출력 파일 기본명
    voxel_size : float
        복셀 크기
    scale : float
        큐브 스케일
    generate_all : bool
        모든 형식 생성 여부 (SCAD, STL, VTK, VTU)
        
    Returns:
    --------
    List[List[int]]
        폴리큐브 좌표
    """
    # 메시를 폴리큐브로 변환
    coords = mesh_to_polycube(input_file, voxel_size)
    
    if generate_all:
        # OpenSCAD 형식 생성
        pc = polycube(coords, scale)
        scad_file = f"{output_base}.scad"
        scad_render_to_file(pc, scad_file)
        print(f"SCAD 파일 생성: {scad_file}")
        
        # STL 생성 (OpenSCAD 필요)
        try:
            scad_to_stl(pc, output_base)
            print(f"STL 파일 생성: {output_base}.stl")
        except Exception as e:
            print(f"STL 생성 실패 (OpenSCAD 필요): {e}")
    
    # VTK 형식 생성
    save_vtk(coords, output_base, scale)
    
    # VTU 형식 생성
    save_vtu(coords, output_base, scale)
    
    return coords

def batch_convert(input_files: List[str],
                 output_dir: str = ".",
                 voxel_size: float = 1.0,
                 scale: float = 12.0,
                 format: str = 'vtk') -> dict:
    """
    여러 메시 파일을 일괄 변환합니다.
    
    Parameters:
    -----------
    input_files : List[str]
        입력 파일 리스트
    output_dir : str
        출력 디렉토리
    voxel_size : float
        복셀 크기
    scale : float
        큐브 스케일
    format : str
        출력 형식
        
    Returns:
    --------
    dict
        변환 결과 정보
    """
    import os
    
    results = {}
    for input_file in input_files:
        basename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, basename)
        
        try:
            coords = convert_mesh_to_vtk(
                input_file, output_file, voxel_size, scale, format
            )
            results[input_file] = {
                'success': True,
                'cube_count': len(coords),
                'output': f"{output_file}.{format}"
            }
        except Exception as e:
            results[input_file] = {
                'success': False,
                'error': str(e)
            }
    
    return results