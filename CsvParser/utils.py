import pandas


AGENCIES = './data/agencies.csv'
COMPONENTS = './data/components.csv'
CONSTRAINTS = './data/constraints.csv'
PROJECTS = './data/projects.csv'
PROPOSALS = './data/proposals.csv'
USER_TYPES = './data/user_types.csv'


# def parseAgencies(filename):

#     pass


# def parseComponents(filename):
#     pass


# def parseConstraints(df):
#     ret = []
#     for i, row in df.iterrows():
#         ret.append({
#             'lat': row['latitude'],
#             'lng': row['longitude'],
#             'max_projects': row['max_projects']
#         })

#     return ret


# def parseProjects(filename):
    
#     return None


# def parseProposals(filename):
#     return None


# def parseUser_types(filename):
#     return None


def parseCsv(filename):
    df = pandas.read_csv(filename)
    cols = list(df.columns)     # list of string
    ret = []
    for i, row in df.iterrows():
        dk = dict()
        for col in cols:
            dk[col] = row[col]

        ret.append(dk)
    
    return ret
