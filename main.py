import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def from_df_to_np_array(df):
    df_label = df.ix[:,:1]
    for i in range(len(df.ix[:,:1])):
        row = df.iloc[i]
        columns = list(df.columns.values)
        c = [[0 for y in range(len(columns))] for x in range(len(df_label))]
        for j in range(len(columns)):
            c[i][j] = row[columns[j]]
    #Numpy takes the matrix and creates the Numpy array
    return np.array(c)

def main(F, sheet, k):

    df3 = pd.ExcelFile(F).parse(sheet)


    df = df3.ix[:,3:] #this will get rid of Names and Matches played for now, because they are just labels
    df_label = df3.ix[:,:1]#this will be the names table, for reference.
    df_mplayed = df3.ix[:,1:2] #this are match played

    #Define the list of features
    columns = list(df.columns.values)
    #Allocate some memory for the matrix using a zeroes matrix
    c = [[0 for y in range(len(columns))] for x in range(len(df_label))]

    #Fill: row is the subset of columns with index i (yes, the i-th row), and fills the c matrix
    for i in range(len(df_label)):
        row = df.iloc[i]
        for j in range(len(columns)):
            c[i][j] = row[columns[j]]
    #Numpy takes the matrix and creates the Numpy array
    X = np.array(c)

    # We create a kmeans class with k number of clusters
    kmeans = KMeans(n_clusters = k)

    #And we set up the cluster process
    kmeans.fit(X)
    centroids = kmeans.cluster_centers_ #centroids coordinates
    #Careful with the final underscore

    #Let's create a dict with all the players on each cluster.
    #To do so, we need to define distance to the centroid.

    def dist_to_nth_centroid(arr,n):
        length = len(arr)
        sum = 0
        centroid_n = centroids[n]
        for i in range(length):
            sum += (arr[i]-centroid_n[i])**2
        return sum

    #Now, for each element in X we are calculating the distance to each centroid,
    #and append its name into the list under the i-th centroid.

    #Name of players
    names = [list(df_label.values[i]) for i in range(len(df_label))]
    L = len(names) #number of players
    dic = {} #we store players here, under the same index a if they are closest to the a-th centroid
    for n in range(k):
        dic[n] = []

    #i will denote the player (i < L); n the centroid (n < k)


    for i in range(L):
        for n in range(k):
            #Initial values when we start the loop
            if n == 0:
                d = dist_to_nth_centroid(X[i],n)#initial distance value
                x = n #initial cluster value
            else:
                dd = dist_to_nth_centroid(X[i],n)

                #if distance to the new cluster is less than whatever we had before
                if dd < d:
                    d = dd#change distance value
                    x = n #change cluster value

        # After the loop, x is the closest cluster. Let's store the name under the correct cluster
        dic[x].append(names[i])

    z = list(centroids)
    for i in range(0,len(centroids)):
        z = list(centroids[i])
        print "Centroid",i
        for player in dic[i]:
            print player[0],
        print ""
        print ""
        for j in range(len(z)):
            z[j] = round(z[j],1)
            if z[j] > 0.5:
                print columns[j],
                print z[j]
        print ""
    return dic

F = 'DataSet4.xlsx'
sheet ='All'
k = 4

main(F,sheet,k)