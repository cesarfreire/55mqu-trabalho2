def main():
    with open('instances/cucas1.txt', 'r') as file:
        # Leitura dos valores de n (sabores) e C (orçamento)
        n, C = map(float, file.readline().strip().split())

        print(f'n: {n}, C: {C}')

        custos = list(map(int, file.readline().strip().split()))
        print(f'custos: {custos}')

        D = int(file.readline().strip())
        print(f'D: {D}')

        dependencias = {}
        for _ in range(D):
            i, j = map(int, file.readline().strip().split())
            if j not in dependencias:
                dependencias[j] = []
            dependencias[j].append(i)

        print(f'dependencias: {dependencias}')

        m = int(file.readline().strip())
        print(f'm: {m}')

        pessoas = []
        for _ in range(m):
            data = list(map(int, file.readline().strip().split()))
            importancia = data[0]
            num_flavors = data[1]
            flavors = data[2:]
            pessoas.append((importancia, flavors))

        print(f'pessoas: {pessoas}')

if __name__ == '__main__':
    main()
