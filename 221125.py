#!/usr/bin/env python
# coding: utf-8

# # 

# In[32]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'NanumGothic'

get_ipython().magic('matplotlib inline')


# In[33]:


import xlrd
import openpyxl
import re


# In[34]:


movies = pd.read_csv('import_data/TB_CJO_MOVIE/TB_CJO_MOVIE.csv')


# In[35]:


movies.sample(10)


# In[36]:


len(movies['영화명'].unique())


# In[37]:


# 영화명 컬럼의 중복된 문자열(영화제목) 합치기 
test = re.findall('[ㄱ-힣]+', s)
print(test)


# In[38]:


text = movies['영화명'].str.extract('([A-Za-z가-힣0-9]+)')


# In[39]:


text.sample(10)


# In[40]:


movies.loc[3044510, :]


# In[41]:


movies.shape
# 534만 6929명


# In[42]:


len(movies['영화명'].unique()) 


# In[43]:


len(movies['광역시도코드'].unique()) 


# In[44]:


len(movies['시군구코드'].unique()) 


# In[45]:


len(movies['읍면동코드'].unique()) 


# * 3056편의 영화
# * 16개의 광역시도/ 113개의 시군구 / 159개의 읍면동 지역 데이터

# ## 데이터타입
# * Categorical Features - 성별구분코드/영화분류코드/광역시도코드/시군구코드/읍면동코드
# * Ordinal - 오단위연령구분코드
# * discrete - 기준일자/관람객수
# * text - 영화명

# ## 기초통계

# ### (1) Categorical Features
# #### ① 성별구분코드

# In[46]:


movies['성별구분코드'].describe()


# In[47]:


movies['성별구분코드'].hist()


# In[48]:


sns.countplot(movies['성별구분코드'])


# In[49]:


movies['성별구분코드'].value_counts()


# In[50]:


movies['성별구분코드'].value_counts().plot.pie(autopct='%1.1f')


# * 남자 44.9%, 여자 53.7% -> 여자가 조금 더 많다
# 

# #### ② 영화구분코드(장르)

# In[51]:


movies['영화분류코드'].describe()


# In[52]:


movies['영화분류코드'].hist()


# In[53]:


plt.figure(figsize=(20,5))
sns.countplot(movies['영화분류코드'])


# In[54]:


movies['영화분류코드'].value_counts()


# In[55]:


plt.figure(figsize=(20,10))
movies['영화분류코드'].value_counts().plot.pie(autopct='%1.1f')


# * 액션/모험, 드라마, 애니메이션이 전체 파이의 절반이상을 차지
# * 공포, 로맨스, 판타지, 미스터리/범죄, 스릴러, 다큐멘터리, 가족/어린이... 등은 5% 미만
# * => 장르간 양극화가 큼 
# * 근데 장르는 딱 한 가지로 분류가 되네? 보통 이렇게 되기 힘들텐데...

# <참고> 영화분류코드
# 
# * 794 액션/모험
# * 798 드라마
# * 795 애니메이션
# * 51581754 범죄
# * 51581755 어드벤처
# * 796 코메디
# * 51331109 공포
# * 51331113 로맨스
# * 51581756 판타지
# * 51331111 미스터리/범죄
# * 51331114 스릴러
# * 797 다큐멘터리
# * 800 가족/어린이
# .
# .
# .

# In[56]:


# 비인기 장르인 공포 영화에는 어떤 게 있나 보자
movies.loc[movies['영화분류코드']==51331109,:].sample(10)


# In[57]:


movies[movies['영화분류코드']==51331109]


# In[58]:


movies_test = [[]]


# In[59]:


# 공포장르 중 흥행한 작품들
movies.loc[movies['영화분류코드']==51331109].value_counts('영화명')


# * 앗 그런데 중복된 문자열이 있다! -> 영화명 컬럼 전처리 필요

# #### ③ 광역시도코드

# In[60]:


plt.figure(figsize=(20,5))
sns.countplot(movies['광역시도코드'])


# In[61]:


movies['광역시도코드'].value_counts().plot.pie(autopct ='%1.1f')


# * 1100000000 (서울특별시), 4100000000(경기도)의 관람객 비율이 거의 절반

# In[62]:


# 2019년 서울 관객들의 픽?
movies.loc[movies['광역시도코드']==1100000000].value_counts('영화명')


# In[63]:


# 2019년 경기도 관객들의 픽?
movies.loc[movies['광역시도코드']==4100000000].value_counts('영화명')


# In[64]:


# 가장 관객수가 적은 지역인 5000000000(제주), 3100000000(울산) 관객들의 픽은 좀 다를까?
movies.loc[movies['광역시도코드']==5000000000].value_counts('영화명')


# In[65]:


movies.loc[movies['광역시도코드']==3100000000].value_counts('영화명')


# * 관객수가 많은 지역과 적은 지역 모두 비슷한 영화를 선택 : 알라딘 - 극한직업 - 엑시트 - 기생충 - 겨울왕국2 or 어벤져스 엔드게임
# <참고> 2019년 대한민국 박스오피스 순위
# * 극한직업 - 어벤져스 엔드게임 - 겨울왕국2 - 알라딘 - 기생충 - 엑시트
# 
# * top 6가 같고, 순서상에 차이가 있는데 이것은 아마 중복된 영화명 데이터를 합치면 어느 정도 완화가 되지 않을까싶다. 

# #### ④ 시군구코드

# In[66]:


plt.figure(figsize=(100,10))
sns.countplot(movies['시군구코드'])


# In[67]:


movies['시군구코드'].value_counts().plot.pie()


# In[68]:


# 두드러지는 지역이 있는데 잘 안보여서 value_counts로 확인
movies['시군구코드'].value_counts()


# TOP5
# * 4113500000 경기도 성남시 분당구 - 영화관(cgv) 갯수가 많음(4개)
# * 2711000000 대구광역시 중구
# * 1156000000 서울특별시 영등포구
# * 1168000000 서울 강남구
# * 1117000000 서울 용산구
# 
# <->
# * 유독 적은 곳은 경기도 오산시로 3057건 - 관이 작긴 하다. 6관짜리 하나, 8관짜리 하나인데, 관은 하나 빼고 다 100석 이하

# #### ⑤ 읍면동코드

# In[69]:


plt.figure(figsize=(100,10))
sns.countplot(movies['읍면동코드'])


# In[70]:


movies['시군구코드'].value_counts().plot.pie()


# In[71]:


# 두드러지는 지역이 있는데 잘 안보여서 value_counts로 확인
movies['읍면동코드'].value_counts()


# TOP5
# * 1117012800 서울특별시 용산구 한강로3가 = 용산cgv
# * 2820010100 인천광역시 남동구 구월동
# * 1168010700 서울특별시 강남구 신사동     
# * 2623010200 부산광역시 부산진구 전포동    
# * 3014011600 대전광역시 중구 문화동
# 
# <->
# * 경상남도 양산시 삼호동이 42건으로 유독 적은 데이터가 집계... = 소규모 영화관 cgv 양산삼호

# => [가설] 관객수는 관(객석) 갯수에 영향을 많이 받나? [확인하기]

# ### (2) Ordinal

# 오단위연령구분코드

# In[72]:


movies['오단위연령구분코드'].describe()


# In[ ]:


movies['오단위연령구분코드'].hist()


# In[ ]:


sns.countplot(movies['오단위연령구분코드'])


# In[ ]:


movies['오단위연령구분코드'].value_counts().plot.pie(autopct='%1.1f')

# 20세~50대 중반(3~9)이 80.3%


# #### 오단위연령구분코드 정보
# * 01 - 14세 이하
# * 02 - 15~19세
# * 03 - 20~24세
# * 04 - 25~29세
# * 05 - 30~34세
# * 06 - 35~39세
# * 07 - 40~44세
# * 08 - 45~49세
# * 09 - 50~54세
# * 10 - 55~59세
# * 11 - 60세이상
# * 99 - 미식별

# #### -> 조금 더 직관적인 분류인 생애주기별 연령구분으로 전처리 
# * 영·유아(0~5세)
# * 아동(6~12세)
# * 청소년(13~18세)
# * 청년(19~29세)
# * 중년(30~49세)
# * 장년(50~64세)
# * 노년(65세 이상)

# ### (3) discrete

# #### ① 기준일자

# In[ ]:


movies['기준일자'].describe()


# In[ ]:


from datetime import datetime

datetime.fromtimestamp()


# In[ ]:


plt.figure(figsize=(30,10))
sns.countplot(movies['기준일자'])


# In[ ]:


sns.kdeplot(data=movies, x='기준일자')


# In[ ]:


movies['기준일자'].value_counts()


# #### ② 관람객수

# In[ ]:


movies['관람객수'].describe()


# In[ ]:


movies['관람객수'].hist()


# In[ ]:


plt.figure(figsize=(30,10))
sns.kdeplot(movies['관람객수'])


# In[ ]:


plt.figure(figsize=(20,10))
movies['관람객수'].value_counts().plot.pie(autopct='%1.1f')


# * power law distribution 

# In[ ]:


movies['관람객수'].value_counts().head(50)


# In[ ]:


# 정규표현식 -> 월별 관람객수 count


# ### (4) 문자형 
# * 영화명 전처리

# ## 피처간 관계찾기와 시각화

# In[ ]:


movies_corr = movies.corr()


# In[ ]:


plt.figure(figsize=(30,10))
sns.heatmap(movies_corr, annot=True)


# * 0에 가까울수록 : 둘 간의 별 관계가 없다(상관관계가 낮음) 
# * 두 피처가 1에 가까울수록(양의 상관관계) : 두 피처가 자주 같이 출현 -> 성별코드, 오단위연령구분코드????
# * 두 피처가 -1에 가까울수록(음의 상관관계) : 두 피처가 아주 드물게 출현, 겹치는 영역이 없음(음의 상관관계가 높음)

# # 인스타 해시태그 인기게시글

# ## Read Data

# In[ ]:


get_ipython().system('pip install xlrd')


# In[ ]:


get_ipython().system('pip install openpyxl')


# In[ ]:


moviegoods = pd.read_excel('upload/moviegoods.xlsx', engine='openpyxl')


# ### goods

# In[ ]:


moviegoods


# In[ ]:


moviegoods['tags']


# In[ ]:


moviegoods['tags_processed']= moviegoods['tags'].str.extract('(\#[A-Za-z가-힣0-9]+)')


# In[ ]:


moviegoods['tags_processed']


# In[ ]:


# 모두 찾기
result = re.findall('\#[A-Za-z가-힣0-9]+', 데이터집합)


# In[ ]:


goods = pd.read_excel('upload/goods.xlsx', engine='openpyxl')


# In[ ]:


goods


# In[ ]:


goods['tags_processed']= goods['tags'].str.extract('(\#[A-Za-z가-힣0-9]+)')


# In[ ]:


goods['tags_processed']


# ### 2019 대한민국 박스오피스 1~6위 영화이름

# In[ ]:


extremejob = pd.read_excel('upload/extramejob.xlsx', engine='openpyxl')


# In[ ]:


extremejob


# In[ ]:


extremejob['tags_processed']= extremejob['tags'].str.extract('(\#[A-Za-z가-힣0-9]+)')


# In[ ]:


extremejob['tags_processed']


# In[ ]:


frozen2 = pd.read_excel('upload/frozen2.xlsx', engine='openpyxl')


# In[ ]:


frozen2


# In[ ]:


frozen2['tags_processed']= frozen2['tags'].str.extract('(\#[A-Za-z가-힣0-9]+)')


# In[ ]:


frozen2['tags_processed']


# In[ ]:


endgame = pd.read_excel('upload/endgame.xlsx', engine='openpyxl')


# In[ ]:


endgame


# In[ ]:


endgame['tags_processed']= endgame['tags'].str.extract('(\#[A-Za-z가-힣0-9]+)')


# In[ ]:


endgame['tags_processed']


# In[ ]:


aladin = pd.read_excel('upload/aladin.xlsx', engine='openpyxl')


# In[ ]:


aladin


# In[ ]:


aladin['tags_processed']= aladin['tags'].str.extract('(\#[A-Za-z가-힣0-9]+)')


# In[ ]:


aladin['tags_processed']


# In[ ]:


parasite = pd.read_excel('upload/parasite.xlsx', engine='openpyxl')


# In[ ]:


parasite


# In[ ]:


parasite['tags_processed']= parasite['tags'].str.extract('(\#[A-Za-z가-힣0-9]+)')


# In[ ]:


parasite['tags_processed']


# In[ ]:


movieexit = pd.read_excel('upload/exit.xlsx', engine='openpyxl')


# In[ ]:


movieexit


# In[ ]:


movieexit['tags_processed']= movieexit['tags'].str.extract('(\#[A-Za-z가-힣0-9]+)')


# In[ ]:


movieexit['tags_processed']


# ## 추천시스템 만들기

# ### 평가지표

# In[ ]:


import numpy as np
from sklearn.metrics import mean_squared_error


# In[ ]:


rmse = np.sqrt(mse)

