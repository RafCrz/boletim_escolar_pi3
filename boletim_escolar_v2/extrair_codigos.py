import os

# Caminho da pasta raiz do projeto
project_path = "D:\\My Documents\\Download\\Curso Django\\Projetos\\VisualCode\\Boletim_online_v2\\boletim_escolar_v2"
output_file = "D:\\My Documents\\Download\\Curso Django\\Projetos\\VisualCode\\Boletim_online_v2\\codigo_projeto.txt"

# Tipos de arquivos a serem incluídos no txt final
file_extensions = ['.py', '.html', '.css', '.js']

def extract_code_from_project(project_path, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if any(file.endswith(ext) for ext in file_extensions):
                        file_path = os.path.join(root, file)
                        outfile.write(f"\n\n# {'-'*50}\n")
                        outfile.write(f"# Arquivo: {file_path}\n")
                        outfile.write(f"# {'-'*50}\n\n")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                outfile.write(infile.read())
                        except Exception as e:
                            print(f"Erro ao ler o arquivo {file_path}: {e}")
        print(f"Códigos extraídos para o arquivo: {output_file}")
    except Exception as e:
        print(f"Erro ao escrever no arquivo de saída: {e}")

# Executa a função
extract_code_from_project(project_path, output_file)
