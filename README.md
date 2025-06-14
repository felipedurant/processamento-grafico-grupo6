# Ray Tracing

### Importante para executar o projeto
- Download da lib Pillow (pip install Pillow)

## Arquivos do Projeto

### "camera.py"
- Importação de bibliotecas para a operação da câmera
- Classe **Camera** contendo os seguintes métodos:
  - "**__init__**" : 
    - Inicializa a câmera com posição, alvo, distância da tela, altura e largura da tela, e vetor para cima.
  - "**get_target_vector**" : 
    - Calcula o vetor direcionado do ponto de posição da câmera até o ponto de alvo.
  - "**set_screen_heigth**" e "**set_screen_width**" : 
    - Definem a altura e largura da tela, ajustando para valores mínimos de 1 se necessário.
  - "**set_vector_up**" : 
    - Define e normaliza o vetor para cima da câmera.
  - "**put_ray_in_start_position**" : 
    - Posiciona o raio na posição inicial, ajustando-o para o topo esquerdo da tela.
  - "**start_ray_cast**" : 
    - Faz o raycasting para todos os pixels da tela, verificando interseções com objetos e colorindo os pixels com base nas colisões.
  - "**verify_intersections**" : 
    - Verifica se o raio colide com objetos na cena e retorna um dicionário de interseções.
  - "**get_closest_object**" : 
    - Determina qual objeto está mais próximo do ponto de origem do raio.

### "image.py"
- Função "**generate_image**":
  - Cria e salva uma imagem no formato PPM com base em uma matriz de cores.
  - Converte o arquivo PPM para JPG usando a biblioteca PIL.
- Função "**ppm_to_jpg**": 
  - Abre um arquivo PPM e o salva como JPG.

### "main.py"

- Inicialização da Câmera: 
  - Define a largura e altura da imagem e inicializa a câmera.
- Inicialização do Plano:
  -  Cria um plano com um ponto, vetor normal e material.
- Funções de Geração de Imagens:
  - Cada função gera uma imagem com diferentes configurações de esferas e planos na cena:
    - **gerar_imagem_longe_da_camera**
    - **gerar_imagem_perto_da_camera**
    - **gerar_imagem_esquerda_e_acima**
    - **gerar_imagem_direita_e_acima**
    - **gerar_imagem_dois_circulos**
    - **gerar_imagem_planos**

- A saída será o código .ppm da respectiva imagem gerada e o arquivo .jpg (6 Imagens no total)

### "mesh.py"
- Classe **Material**:
  - Representa as propriedades físicas de um material, como cor, coeficiente especular, lambertiano, ambiental, tipo de material, índice de refração e componente transmissiva.

### "object.py"
- Classe Abstrata **Object**:
  - Define métodos abstratos "intersects" e "get_color" que devem ser implementados por subclasses.

### "plane.py"
- Classe **Plane**:
  - Representa um plano definido por um ponto, vetor normal e material.
  - Métodos para inicialização, representação textual, cálculo de interseções com um raio, normal da superfície e cor do material.

### "point.py"
- Classe **Point**:
  - Representa um ponto no espaço 3D com coordenadas x, y, z.
  - Métodos para operações aritméticas, cálculo de distância, ponto médio, movimento em direção a outro ponto, cálculo de coordenadas baricêntricas e determinação do ponto mais próximo em uma lista.

### "point_light.py"
- Classe **Light**:
  - Representa uma fonte de luz com posição e cor.
  - Método para retornar a posição da fonte de luz.

### "ray.py"
- Classe **Ray**:
  - Representa um raio com origem e direção.
  - Métodos para inicialização, obtenção de um ponto por parâmetro ou distância, inversão da direção do raio, configuração e alteração da direção, e representação textual.

### "sphere.py"
- Classe **Sphere**:
  - Representa uma esfera com centro, raio e cor.
  - Método "intersects" para calcular se um raio intersecta a esfera e retornar o ponto de interseção.

Essa é uma visão geral das funcionalidades e métodos principais em cada arquivo do projeto. 
