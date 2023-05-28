import pandas as pd

file_path="C:/Users/umitg/Downloads/SecimSonucIl.json"

df = pd.read_json(file_path)
df.columns = ['Plaka', 'İl', 'Kayıtlı Seçmen Sayısı', 'Oy Kullanan Seçmen Sayısı',
            'Geçerli Oy Toplamı', 'MUHARREM İNCE', 'MERAL AKŞENER',
            'RECEP TAYYİP ERDOĞAN', 'SELAHATTİN DEMİRTAŞ',
            'TEMEL KARAMOLLAOĞLU', 'DOĞU PERİNÇEK']

df = df.drop(df.index[df.index % 2 != 0])

df['Geçerli Oy Toplamı'] = df['Geçerli Oy Toplamı'].str.replace('.','').astype(int)
df['MUHARREM İNCE'] = df['MUHARREM İNCE'].str.replace('.','').astype(int)
df['MERAL AKŞENER'] = df['MERAL AKŞENER'].str.replace('.','').astype(int)
df['RECEP TAYYİP ERDOĞAN'] = df['RECEP TAYYİP ERDOĞAN'].str.replace('.','').astype(int)
df['SELAHATTİN DEMİRTAŞ'] = df['SELAHATTİN DEMİRTAŞ'].str.replace('.','').astype(int)
df['TEMEL KARAMOLLAOĞLU'] = df['TEMEL KARAMOLLAOĞLU'].str.replace('.','').astype(int)
df['DOĞU PERİNÇEK'] = df['DOĞU PERİNÇEK'].str.replace('.','').astype(int)

e={}
k=0
for x in range(4,len(df.columns)):
    k += 1
    e={df.columns[x]:k}

print(e)

