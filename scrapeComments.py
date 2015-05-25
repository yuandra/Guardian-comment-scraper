from bs4 import BeautifulSoup
import urllib

def getHTML(url):
    html = urllib.urlopen(url).read()
    return BeautifulSoup(html)

def scrapeComments(url):
    articleSoup = getHTML(url)
    articleTitle = articleSoup.find('h1', class_="content__headline").getText().strip().encode('utf-8')
    commentUrl = articleSoup.find(class_='discussion__heading').find('a')['href']

    print 'Finding comments for [{0}]({1})\n'.format(articleTitle, url)

    commentSoup = getHTML(commentUrl)

    paginationBtns = commentSoup.find_all('a', class_='pagination__action')
    LastPaginationBtn = commentSoup.find('a', class_='pagination__action--last')

    if LastPaginationBtn is not None:
        totalPages = int(LastPaginationBtn['data-page'])
    elif paginationBtns:
        totalPages = int(paginationBtns[-1]['data-page'])
    else:
        totalPages = 1

    def getComments(url):
        soup = getHTML(url)
        print 'Fetching {0}'.format(url)
        commentArray = []
        for comment in soup.select('li.d-comment'):
            commentObj = {}
            commentObj['id'] = comment['data-comment-id']
            commentObj['timestamp'] = comment['data-comment-timestamp']
            commentObj['author'] = comment['data-comment-author'].encode('utf-8')
            commentObj['author-id'] = comment['data-comment-author-id']
            # commentObj['reccomend-count'] = comment.find(class_='d-comment__recommend')['data-recommend-count']

            body = comment.find(class_='d-comment__body')
            if body.blockquote is not None:
                body.blockquote.clear()
            commentObj['text'] = body.getText().strip().encode('utf-8')

            replyTo = comment.find(class_='d-comment__reply-to-author')
            if replyTo is not None:
                link = replyTo.parent['href'].replace('#comment-', '')
                commentObj['reply-to'] = link
            else:
                commentObj['reply-to'] = ''

            commentArray.append(commentObj)
        commentArray = commentArray[::-1]
        return commentArray

    allComments = []

    for i in range(totalPages, 0, -1):
        params = urllib.urlencode({'page': i})
        url = '{0}?={1}'.format(commentUrl, params)
        pageComments = getComments(url)
        allComments = allComments + pageComments

    return allComments
