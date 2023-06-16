import numpy as np
import pandas as pd
from rdchiral.template_extractor import extract_from_reaction
from rdkit import Chem
from rdkit.Chem import AllChem
import openpyxl

final_list = np.array([[0,0]])
num = 0

def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])
def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

def get_reaction(data):
    id = data[0]
    reactants, products = data[2].split('>>')
    inputRec = {'_id':id, 'reactants':reactants, 'products':products}
    ans = extract_from_reaction(inputRec)
    if 'reaction_smarts' in ans.keys():
        return reactants, products, ans['reaction_smarts']
def code_from_product(product):
    mol = Chem.MolFromSmiles(product)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    onbits = list(fp.GetOnBits())
    arr = np.zeros(fp.GetNumBits(), dtype=np.bool8)
    arr[onbits] = 1
    return arr

def df_2_code(df):
    global num
    global final_list
    num = num+1
    reactants, products, smarts = get_reaction(df)
    product_code = code_from_product(products)
    product_num = np.sum(product_code)
    template_code = encode(smarts)
    template_code = template_code.replace(' ', '')
    template_num = np.sum(np.array(list(template_code), dtype=np.uint8))
    temp = np.array([[product_num, template_num]])
    final_list = np.append(final_list, temp, axis=0)

    print(final_list.shape)
    print('schedule: ', num/40009)
    pass


def load_data(path,name):
    global final_list
    global num
    ex = openpyxl.load_workbook(name)
    sheet = ex['Sheet1']

    data = pd.read_csv(path)
    final_list = np.array([[0,0]])
    num = 0
    data.apply(func=df_2_code,axis=1,raw=False)
    final_list = np.delete(final_list, 0, axis=0)

    num = 0
    print('11111: ',final_list.shape)
    for i in final_list:
        num = num+1
        print('save schedule: ', num/40009)
        sheet.append(list(i))
    ex.save(name)
    pass



if __name__=='__main__':
    path = r'schneider50k/raw_test.csv'
    name = r'test.xlsx'

    load_data(path,name)
    pass