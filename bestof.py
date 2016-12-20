import string, praw, time, io



def Main():

    weeks_to_scan = 52
    epoch_today = time.time()
    
    #Variables to change
    subname = 'photoshopbattles'    
    output_file = 'C:\\best.csv'
    minimum_karma_threshold = 100


    #Column name array
    column_headers = []
                            
    column_headers.append('Submission_Title')
    column_headers.append('Submission_Url')
    column_headers.append('Submission_Author')
    column_headers.append('Submission_Score')
    column_headers.append('Submission_Short_Link')
    column_headers.append('Submission_Created_Epoch')
    column_headers.append('Submission_Created_GMT')
    column_headers.append('Comment_Body')
    column_headers.append('Comment_Author')
    column_headers.append('Comment_Score')
    column_headers.append('Comment_Link')

    #Format the headers into a pipe delimited string
    delimited_column_headers = '|'.join(column_headers)
    print(delimited_column_headers)

    #Create the output file and write headers to it
    f = open(output_file, 'w')
    f.write(delimited_column_headers + '\r\n')
    f.close()
    

    #Login
    #r = praw.Reddit(user_agent)
    r = praw.Reddit(client_id='change_this', client_secret='change_this', user_agent='change_this')
    #r.login(username, password, disable_warning=True)


    #Get the top submissions for the year
    sub = r.subreddit(subname)

    for week in range(0, weeks_to_scan):

        print('Scanning week ' + str(week))
        
        epoch_from = epoch_today - (604800 + (604800 * week))
        epoch_to = epoch_today - (604800 * week)

        search_string = 'timestamp:' + str(int(epoch_from)) + '..' + str(int(epoch_to))

        submissions = sub.search(search_string, syntax='cloudsearch', limit=None)

        ScanSubmissions(r, submissions, output_file, minimum_karma_threshold)


def ScanSubmissions(r, submissions, output_file, minimum_karma_threshold):

    #Go through each submission
    for submission in submissions:

        try:

            #Disregard deleted or removed posts
            if submission.author and submission.banned_by == None:

                #Get the comments
                #submission.replace_more_comments(limit=None, threshold=0)
                #comments = praw.helpers.flatten_tree(submission.comments)
                submission.comments.replace_more(limit=None)

                #Disregard submissions with no comments
                if submission.comments:

                    #Go through each comment
                    for comment in submission.comments.list():

                        try:

                            #Disregard deleted comments
                            if comment.author:
                                
                                karma = int(comment.score)

                                #Disregard removed comments and comments below the karma threshold
                                if karma > minimum_karma_threshold and comment.banned_by == None:

                                    #Populate data into an array
                                    row = []
                            
                                    row.append(str(submission.title))  #Submission_Title
                                    row.append(str(submission.url).replace('\r',' '))  #Submission_Url
                                    row.append('/u/' + str(submission.author.name))  #Submission_Author
                                    row.append(str(submission.score))  #Submission_Score
                                    row.append('https://redd.it/' + str(submission.id))  #Submission_Short_Link
                                    row.append(str(submission.created_utc))  #Submission_Created_Epoch
                                    row.append(str(time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(float(submission.created_utc)))))  #Submission_Created_GMT
                                    row.append(str(comment.body).replace('\r',' ').replace('\n',' ').replace('\t',' '))  #Comment_Body
                                    row.append('/u/' + str(comment.author.name))  #Comment_Author
                                    row.append(str(comment.score))  #Comment_Score
                                    row.append('https://np.reddit.com/comments/' + submission.id + '/-/' + comment.id + '?context=1000')  #Comment_Link

                                    #Format the row into a pipe delimited string
                                    delimited_row = '\t'.join(row)
                                    print(delimited_row)

                                    #Append the row to the output file
                                    f = open(output_file, 'a')
                                    f.write(delimited_row + '\r\n')
                                    f.close()

                        except (Exception) as e:

                            print(e)

        except (Exception) as e:

            print(e)



    return




Main()
