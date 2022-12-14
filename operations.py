import vaex
import os
import pandas

def merge_frames(paths:list, new_filename:str = 'merged.hdf5'):
    df = vaex.open_many(paths)

    df.export_hdf5(new_filename)

    print(f'Merged file exported as {new_filename}')

    return new_filename

def remove_duplicates_from_df(dataframe):
    '''
    Args:
        dataframe should be a pandas df
    '''
    clean_df = dataframe.drop_duplicates()
    return clean_df



def remove_duplicates_from_file(path:str):
    '''
    Args:
        path: path as a string without extension
    '''
    data = vaex.open(f'{path}.hdf5')

    pandas_data = data.to_pandas_df()
    clean_df = pandas_data.drop_duplicates()

    v_clean = vaex.from_pandas(clean_df)

    export_loc = f'{path}_cleaned.hdf5'

    v_clean.export_hdf5(export_loc)

    print(f'Clean file exported as {export_loc}')

    return export_loc

if __name__ == "__main__":
    remove_duplicates_from_file('corpus_fr_marioupol_2022-03-14_to_2022-03-30')


