
## Project Report by AV David

<br>

### Problem Statement

This project aims to address the problem, **"Create an alogrithm that will recommend books to readers."**


---

### Executive Summary

In this project, over 91,000 ratings (integers from 1 to 5, with 1 being the "bad book" and 5 being the "great book") of over 7,600 readers of over 3,500 books were utilized in creating an algorithm to recommend books to existing and new readers. For the purpose of this report, "items" and "books", and "users" and "readers", are used interchangeably. 

The method used in this project is collaborative filtering, a technique used in designing recommender systems using feedback from users on various items. Two types of collaborative filtering were tested and compared: memory-based and model-based. Memory-based algorithms use the ratings to create a similarity matrix of items (or users). Based on this similarity matrix, top most similar items (or users) -- also referred to as "nearest neighbors" -- are aggregated to calculate an estimated rating.  In this problem, for a memory-based algorithm, an item-based approach (similarities were computed between items) performed better than user-based approach (similarities computed between users). 

On the other hand, model-based algorithms utilize more complex computations/deep learning to "learn" the characteristics of items and users. A specific model-based approach tested in this project is matrix factorization, wherein a model predicts various "latent factors" that are similar between the items and the users using patterns in the ratings.

The metric used to evaluate the models was root mean squared error in order to get a sense of the difference between the estimated rating and the actual rating.  After trying various models, the top two models were:

|Approach|Type|Algorithm|RMSE|
|---|---|---|---|
|Memory-Based|<center>Item-based</center>|<center>KNNBaseline</center>|<center>0.5638 </center>|
|Model-Based|<center>Matrix Factorization</center>|<center>Non-negative Matrix Factorization (NMF)</center>|<center>0.7587 </center>|

<br>

KNN had an average rating error of 0.35 points while NMF had an average rating error or 0.56 points. While KNN performed better, it also took longer to process the data, especially for existing users. Due to accuracy and processing time considerations, KNN is recommended for new users while NMF is recommend for existing users.


---

### File Directory

I have included the following in this report:

- README.md
- Data folder
    - Data collected from Goodreads Dataset
    - Sample file that was used for modeling
- Code folder
    - Data Collection and Cleaning
    - Sample EDA
    - KNN models
    - Matrix Factorization-based models
    - Comparison of KNN and NMF
    - Creating output information
    - NMF Predictions: Existing users
    - KNN Predictions: New users
- Streamlit app folder
- Presentation folder
    - Presentation pdf

---

### Data Dictionary

|Feature|Type|Dataset|Description|
|---|---|---|---|
|**book_id**|*int*|Books Reviews/Info|Unique ID assigned to a book|
|**title**|*object*|Books Reviews/Info|Title of the book|
|**user_id**|*object*|Books Reviews|Unique ID assigned to a reader|
|**rating**|*int*|Books Reviews|Rating given by reader|
|**Author**|*object*|Books Info|Name of author|
|**Publication Year**|*object*|Books Info|The year book was published|


---

### Conclusions and Recommendations

Based on the exploration and modeling of the data, below are my findings and recommendations:

1. KNN model performed better than NMF in estimating true ratings of existing users. However, the processing time for KNN was 4 times that of NMF.
2. Due to accuracy, processing time, and file size considerations, I recommend a hybrid approach:
    - Use KNN to make recommendations for new users and NMF for existing users. The advantage of using KNN for new users is the ease of explainability of results such as "Since you liked book A, here are books similar to book A according to ratings by X number of readers." 
    - For existing users, NMF processes data much faster, so although it predicts ratings little less accurately than KNN, I would recommend NMF based on efficiency.
3. For further research, I would recommend looking into other model-based algorithms such as neural nets and trying other libraries like fastai. Only the Suprise library was used for this project. 
4. For the streamlit app, design for user input could be better such as taking keywords to search for titles. The current version only takes actual titles (with very specific lettercase and punctuations) as input.


---

### Sources and References

Data for this project was collected from the [2017 Goodreads dataset](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home), which originally consisted of over 2.36 million books from various genres, 870,000 users, and 100 million ratings. Due to file size and processing time, a subset was taken from only one genre, Children's Books.

- [Surprise docs](https://surprise.readthedocs.io/en/stable/)
- [Lecture on collaborative filtering](https://youtu.be/h9gpufJFF-0)
- [Collaborative filtering on Wikipedia](https://en.wikipedia.org/wiki/Collaborative_filtering)