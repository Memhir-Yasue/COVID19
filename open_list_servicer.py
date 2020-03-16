import pandas as pd


def count_cases(df):
    cases_dict = {}
    for i in range(len(df)):
        city = df.iloc[i][0]
        province = df.iloc[i][1]
        country = df.iloc[i][2]

        if country not in cases_dict:
            cases_dict[country] = {}
        if province not in cases_dict[country]:
            cases_dict[country][province] = {}
        if province in cases_dict[country]:
            if city not in cases_dict[country][province]:
                cases_dict[country][province][city] = 1
            else:
                cases_dict[country][province][city] += 1
    return cases_dict


def append_cases(df_in, cases_dict):
    df = df_in.drop_duplicates().reset_index(drop=True)
    case_dict = {'case': []}
    for i in range(len(df)):
        get_city = df.iloc[i][0]
        get_province = df.iloc[i][1]
        get_country = df.iloc[i][2]
        get_case_num = cases_dict[get_country][get_province][get_city]
        case_dict['case'].append(get_case_num)

    case_df = pd.DataFrame(case_dict)
    df['case'] = case_df['case']
    return df

def run_open_list():
    df_raw = pd.read_csv('data/COVID19_2020_open_line_list - outside_Hubei.csv')
    df_na = df_raw[['city', 'province', 'country', 'latitude', 'longitude']]
    df = df_na.dropna(subset=['latitude','longitude','country'])

    cases = count_cases(df)
    neo_df = append_cases(df,cases)
    return neo_df