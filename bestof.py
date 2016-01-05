# Best-Of
import praw, OAuth2Util, time, io



def Main():

    #Variables to change
    subname = 'photoshopbattles'
    username = '_korbendallas_'
    user_agent = '_korbendallas_ by /u/_korbendallas_ ver 0.1'
    minimum_karma_threshold = 999
    output_file = 'C:\\best.csv'


    #Column name array
    column_headers = []
                            
    column_headers.append('Submission_Title')
    column_headers.append('Submission_Body')
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
    print delimited_column_headers

    #Create the output file and write headers to it
    f = open(output_file, 'w')
    f.write(delimited_column_headers + '\r\n')
    f.close()
    

    #Login
    r = praw.Reddit(user_agent)
    o = OAuth2Util.praw.AuthenticatedReddit.login(r, disable_warning=True)


    #Get the top submissions for the year
    sub = r.get_subreddit(subname)

    submissions = sub.get_top_from_year(limit=None)


    #Go through each submission
    for submission in submissions:

        try:

            #Disregard deleted or removed posts
            if submission.author and submission.banned_by == None:

                #Get the comments
                submission.replace_more_comments(limit=None, threshold=0)
                comments = praw.helpers.flatten_tree(submission.comments)

                #Disregard submissions with no comments
                if comments:

                    #Go through each comment
                    for comment in comments:

                        try:

                            #Disregard deleted comments
                            if comment.author:

                                karma = int(comment.score)

                                #Disregard removed comments and comments below the karma threshold
                                if karma > minimum_karma_threshold and comment.banned_by == None:

                                    #Populate data into an array
                                    row = []
                            
                                    row.append(str(submission.title))  #Submission_Title
                                    row.append(string.replace(str(submission.body),'\r','  '))  #Submission_Body
                                    row.append('/u/' + str(submission.author.name))  #Submission_Author
                                    row.append(str(submission.score))  #Submission_Score
                                    row.append(str(submission.short_link))  #Submission_Short_Link
                                    row.append(str(submission.created_utc))  #Submission_Created_Epoch
                                    row.append(str(time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(float(submission.created_utc)))))  #Submission_Created_GMT
                                    row.append(string.replace(str(comment.body),'\r','  '))  #Comment_Body
                                    row.append('/u/' + str(comment.author.name))  #Comment_Author
                                    row.append(str(comment.score))  #Comment_Score
                                    row.append(string.replace(str(comment.permalink), 'www.reddit.com', 'np.reddit.com') + '?context=1000')  #Comment_Link

                                    #Format the row into a pipe delimited string
                                    delimited_row = '|'.join(row)
                                    print delimited_row

                                    #Append the row to the output file
                                    f = open(output_file, 'a')
                                    f.write(delimited_row + '\r\n')
                                    f.close()

                        except (Exception) as e:

                            print e.message

        except (Exception) as e:

            print e.message



    return




Main()
