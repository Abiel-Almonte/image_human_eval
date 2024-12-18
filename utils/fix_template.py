import pandas

COLS= [
    'Class Number',
    'Image Number',
    'Prompt Number',
    'Quality',
    'Aesthetics',
    'ADDITION',
    'SPECIFIC OBJECT',
    'CHANGE',
    'STYLE TRANSFER',
    'BACKGROUND',
    'SPECIFIC DETAIL',
    'SPECIFIC POSITION',
    'LANDSCAPE',
    'COUNT',
    'ENTIRE OBJECT-RELEVANT',
    'ENTIRE OBJECT-IRRELEVANT',
    'FICTION REFERENCE',
    'TIMELINE',
    'IMAGE',
    'CAMERA CONTROL',
    'REMOVAL',
    'MULTIPLE-OBJECT'
]

if __name__ == '__main__':
    df= pandas.read_csv('./data/Rating_Template_Final.csv')
    df.drop([0, 1], inplace= True)
    df.columns= COLS
    df.to_csv(f'./data/Rating_Template_Final.csv', index= False)