# Em um novo arquivo: obj_loader.py

from typing import List, Tuple
from point import Point

def load_obj_file(filepath: str) -> Tuple[List[Point], List[tuple]]:
    """
    Lê um arquivo .obj e extrai os vértices e as faces.

    Esta é uma versão simplificada que lê apenas vértices (v) e
    faces triangulares (f). Ignora normais (vn) e texturas (vt).

    Args:
        filepath (str): O caminho para o arquivo .obj.

    Returns:
        Uma tupla contendo duas listas: a lista de vértices (Points)
        e a lista de faces (tuplas de índices).
    """
    vertices = []
    faces = []
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                # Remove espaços em branco no início e no fim da linha
                line = line.strip()

                if not line or line.startswith('#'):
                    # Ignora linhas vazias ou comentários
                    continue

                parts = line.split()
                command = parts[0]

                if command == 'v':
                    # Linha de vértice: v x y z
                    vertices.append(Point(float(parts[1]), float(parts[2]), float(parts[3])))
                
                elif command == 'f':
                    # Linha de face: f v1 v2 v3 ...
                    # O formato pode ser complexo (ex: f 1/1/1 2/2/2 3/3/3)
                    # Extrair apenas o primeiro número (índice do vértice).
                    face_indices = []
                    for part in parts[1:]:
                        # Pega o número antes da primeira '/'
                        vertex_index_str = part.split('/')[0]
                        # Converte para inteiro e SUBTRAI 1 (índices .obj são base 1, Python é base 0)
                        face_indices.append(int(vertex_index_str) - 1)
                    
                    # Este parser simples assume que a face é um triângulo.
                    # Para faces com mais de 3 vértices (quads), ele ainda pega só os 3 primeiros.
                    if len(face_indices) >= 3:
                        faces.append(tuple(face_indices[0:3]))

    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em '{filepath}'")
        raise
    except Exception as e:
        print(f"ERRO: Falha ao ler o arquivo .obj: {e}")
        raise

    print(f"Arquivo .obj carregado: {len(vertices)} vértices, {len(faces)} faces.")
    return vertices, faces