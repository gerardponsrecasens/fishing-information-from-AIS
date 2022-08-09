import pandas as pd

data = pd.read_csv(r'./chlorphyll.csv')
data['Day'] = pd.to_datetime(data['Day'])
data = data.drop_duplicates()
data['grid'] = data['Latitude'].astype(str) +','+ data['Longitude'].astype(str)
cells = data.grid.unique()

weeks = ['11W']

for k in [11]:
    df = []
    shift = 7*k
    for cell in cells:
        work = data[data['grid']==cell]
        n = len(work)
        agg = []
        for i in range(n):
            chlor = 0
            t = 0
            for j in range(7):
                if i-shift-j >=0:
                    if not pd.isnull(work.iloc[i-shift-j,3]):
                        chlor += work.iloc[i-shift-j,3]
                        t +=1
            if t != 0:
                chlor = chlor/t
                agg.append(chlor)
            else:
                agg.append('')
        work['11W'] = agg
        df.append(work)

    all = pd.concat(df)
    dataset = all

dataset.to_csv(r'lag.csv',index = False)  