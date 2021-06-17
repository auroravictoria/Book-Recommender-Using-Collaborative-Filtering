import streamlit as st
import pandas as pd
from surprise import KNNBaseline
from surprise import Dataset, Reader
from collections import defaultdict
from surprise import dump

st.title("Book Recommender")
st.header("Looking for children's books?")
st.subheader("Let's start...")
st.text("")

sample = pd.read_csv('books_reviews_sample.csv')
book_info = pd.read_csv('books_info.csv', index_col=None, 
                     usecols=['book_id', 'Title', 'Author', 'Publication Year'])
ratings = sample[['user_id', 'book_id', 'rating']]

reader = Reader(rating_scale=(1,5))
dataset = Dataset.load_from_df(ratings,reader)

bsl_options = {'method': 'sgd',
               'reg': .08,
               'learning_rate': .005,
               'n_epochs': 40}
              
sim_options = {'name': 'msd',
               'min_support':1,
               'user_based': False}

algo_knn = KNNBaseline(k=40, min_k=2, sim_options = sim_options, bsl_options = bsl_options)
trainset = dataset.build_full_trainset()
algo_knn.fit(trainset)

title_to_bookID = pd.Series(sample.book_id.values, index = sample.title).to_dict()

def getBookID(booktitle):
    if str(booktitle) in title_to_bookID:
        return title_to_bookID[str(booktitle)]
    else:
        return ""

def book_top_neighbors(book_title):
    
    # convert title to book id
    book_id = getBookID(book_title)
    
    # get inner ID of book ID
    book_id_inner = trainset.to_inner_iid(book_id)
        
    # get list of inner IDs of neighbors
    neighbors_inner_id = algo_knn.get_neighbors(book_id_inner, k=10)
    
    # get list of raw IDs
    recom_raw_id_list=[]
    for book_id in neighbors_inner_id:
        book_raw_id = trainset.to_raw_iid(book_id)
        recom_raw_id_list.append(book_raw_id)

    # make a dataframe
    df = pd.DataFrame(recom_raw_id_list, index=list(range(1,11)), columns = ['book_id'])
    merged_df = pd.merge(left=df, right=book_info, how='left', on='book_id')
    merged_df.drop(columns='book_id', inplace=True)
    merged_df.index = merged_df.index + 1
    
    return merged_df

new_user = st.checkbox("Are you a new user?")

if new_user:

    like_book = st.text_input('What book did you like?', 'The Line')
    
    if like_book is not None:
    
        st.write('You entered', like_book)

        recommendations_df = book_top_neighbors(like_book)
      
        st.write('We recommend:')

        st.table(recommendations_df)

@st.cache(suppress_st_warning=True)
def load_preds(file_path):
    preds_nmf, algo_nmf = dump.load(file_path)
    return preds_nmf

file_path = './dump_NMF_small'
preds_nmf = load_preds(file_path)

def get_book_recoms_df(user_id):
    
    top = defaultdict(list)
    
    # Get the list of ratings for the user
    for uid, iid, true_r, est, _ in preds_nmf:
        if uid == user_id:
            top[uid].append((iid, est))
    
    # Sort the list
    for uid, user_ratings in top.items():
        user_ratings.sort(key=lambda x:x[1], reverse = True)
        top[uid] = user_ratings[:10]
    
    # get list of only book IDs
    recom_id_list=[]
    for bookid_ratings_list in top.values():
        for pair in bookid_ratings_list:
            recom_id_list.append(pair[0])
    
    # make a dataframe for recommendations
    df=pd.DataFrame(index=range(1,11))
    df['book_id'] = recom_id_list
    merged_df = pd.merge(left=df, right=book_info, how='left', on='book_id')
    merged_df.drop(columns='book_id', inplace=True)
    merged_df.index = merged_df.index + 1
    
    return merged_df

existing_user = st.checkbox("Are you an existing user?")

if existing_user:
    existing_user_id = st.text_input('What is your user ID?', 'f8bf8e54d6de45b52d2286e733271e34')
    st.write('You entered', existing_user_id)

    recoms = get_book_recoms_df(existing_user_id)

    st.write('Here are the books recommended for you:')

    st.table(recoms)
