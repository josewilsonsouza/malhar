# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:43:54 2024

@author: José Wilson
"""

import pandas as pd
import requests as rq

class TimeStep:
    
    dir = 'https://raw.githubusercontent.com/josewilsonsouza/Machine_Learing_INMETRO/main/Data_Bike_2023'
    
    def __init__(self, number_sample):
        self.number_sample = number_sample
        self.labels = ['duas_maos','mao_direita','mao_esquerda']

    def load_data(self):
        '''
        Função específica para os código do repositório @Machine_Learing_INMETRO.
        Ela carrega a amostra de dados de aceleração triaxial para o trajeto percorrido pelo ciclista.
        Esses dados foram coletados usando o app SensorBox
    
        Parameters
        ----------
            - sample_data: '1', '2' or '3'
        
        Returns:
            Df
        -------
        '''
        
        dfs = [pd.read_csv(f'{self.dir}/amostra_{self.number_sample}_{label}/ACG.csv', sep = ';') for label in self.labels]
            
        return dfs
    
    def load_files_extra(self):
        '''
        Função específica para os código do repositório @Machine_Learing_INMETRO.
        Ela carrega os arquivos 'extra.json' que contém informação do tempo  de 
        percurso do trajeto.
        
        Parameters
        ----------
            - sample_data: '1', '2' or '3'
        
        Returns:
            todos os arquivos 'extra.json' para cada label.
        -------
        '''
        
        files_extra = []  # Lista para armazenar os arquivos extra.json de cada df
    
        for label in self.labels:
            url = f'{self.dir}/amostra_{self.number_sample}_{label}/extra.json'
            response = rq.get(url)
        
            # Verificar se a solicitação foi bem-sucedida (código de status 200)
            if response.status_code == 200:
                data = response.json()
                files_extra.append(data)
                
            else:
                print(f"Falha ao carregar o arquivo JSON para o rótulo '{label}'. Código de status: {response.status_code}")
        
        return files_extra
                
    def time_step(self):
        '''
        Função que ajusta o TimeStamp.

        Returns
        -------
        dataframe : TYPE
            DESCRIPTION.

        '''
        
        dfs = []
        
        for df, dados, label in zip(self.load_data(), self.load_files_extra(), self.labels):

            df["t"] = (((dados["nanos"] - df.t) // 1000000) + dados["millis"]) #aplica correcoes de metadados
            df["t"] = df.t - df.t.min() #puxa tempo inicial para zero, subtraindo valor minimo como offset
            df.sort_values(by = 't', inplace = True) # ordena os dados no tempo
            df.reset_index(drop=True, inplace = True)
            df['label'] = label # para cada df insere sua label
            
            dfs.append(df)
        
        dataframe = pd.concat(dfs) # juntando todos os dfs em um só
        dataframe.drop('a', axis=1, inplace=True)
        return dataframe