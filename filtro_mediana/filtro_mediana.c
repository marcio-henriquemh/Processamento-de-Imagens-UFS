#include <stdint.h>

// Função de filtro de mediana
void filtro_mediana(int largura, int altura, uint8_t* entrada, uint8_t* saida) {
    int linha, coluna, k, viz_linha, viz_coluna, viz_index;
    uint8_t temp[9];

    for (linha = 0; linha < altura; linha++) {
        for (coluna = 0; coluna < largura; coluna++) {
            k = 0;
            for (viz_linha = -1; viz_linha <= 1; viz_linha++) {
                for (viz_coluna = -1; viz_coluna <= 1; viz_coluna++) {
                    viz_index = (linha + viz_linha) * largura + coluna + viz_coluna;
                    if (viz_index >= 0 && viz_index < largura*altura) {
                        temp[k] = entrada[viz_index];
                        k++;
                    }
                }
            }

            // Ordena a matriz de pixels
            for (viz_linha = 0; viz_linha < 9; viz_linha++) {
                for (viz_coluna = viz_linha+1; viz_coluna < 9; viz_coluna++) {
                    if (temp[viz_linha] > temp[viz_coluna]) {
                        uint8_t tmp = temp[viz_linha];
                        temp[viz_linha] = temp[viz_coluna];
                        temp[viz_coluna] = tmp;
                    }
                }
            }

            // Define o valor do pixel de saída para a mediana dos valores ordenados
            saida[linha*largura+coluna] = temp[4];
        }
    }
}
