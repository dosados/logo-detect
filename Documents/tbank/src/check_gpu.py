import torch

print(torch.cuda.is_available())  # True, если CUDA доступна
print(torch.cuda.device_count())  # количество GPU
print(torch.cuda.get_device_name(0))  # имя первого GPU