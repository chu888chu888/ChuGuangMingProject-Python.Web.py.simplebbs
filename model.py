# -*- coding: utf-8 -*-
import datetime
import hashlib
from os.path import join

import web

import util


db = web.database(dbn='sqlite', db=join("data", "forum.db3"))


def count_comment(parent):
    comments = db.select('posts', what='id', where='parent = $parent', vars=locals())
    count = 0
    if not comments:
        return 0
    else:
        for i in comments:
            count += count_comment(i.id) + 1
    return count


def list_comment(parent):
    # comments = db.select('posts', what='id, title, content, datetime(created) as created, user_id',
    #                      where='parent = $parent', order='id DESC', vars=locals())
    # if not comments:
    #     return ''
    # output = '<ul>'
    # for i in comments:
    #     user = db.select('users', what='username', where="id = $i.user_id", vars=locals())[0]
    #     output += '<li><a href="/view/' + str(
    #         i.id) + '">' + i.title + '</a> - <b>' + user.username + '</b> (' + util.humanize_bytes(
    #         len(i.content)) + ') ' + i.created + ' (' + str(count_comment(i.id)) + ')</li>' + list_comment(i.id)
    # output += '</ul>'
    commentsCount = db.query("SELECT COUNT(*) AS count FROM posts where id="+str(parent))[0]
    print commentsCount
    return str(commentsCount.count)


def view_comment(parent):
    comments = db.select('posts', what='id, title, content, datetime(created) as created, user_id',
                         where='parent = $parent', order='id DESC', vars=locals())
    if not comments:
        return ''
    return comments
# 返回列表


def list_post(page):
    # perpage = 20
    # offset = (page - 1) * perpage
    # output = '<ul>'
    # posts = db.select('posts', what='id, title, content, datetime(created) as created, user_id', where='parent = 0',
    #                   offset=offset, limit=perpage, order='id DESC')
    # postcount = db.query("SELECT COUNT(*) AS count FROM posts")[0]
    # pages = postcount.count / perpage
    # if postcount.count % perpage > 0:
    #     pages += 1
    # for i in posts:
    #     user = db.select('users', what='username', where="id = $i.user_id", vars=locals())[0]
    #     output += '<li><a href="/view/' + str(
    #         i.id) + '">' + i.title + '</a> - <b>' + user.username + '</b> (' + util.humanize_bytes(
    #         len(i.content)) + ') ' + i.created + ' (' + str(count_comment(i.id)) + ')</li>'
    #     output += list_comment(i.id)
    # output += '</ul>'
    perpage = 20
    offset = (page - 1) * perpage
    output = ''
    posts = db.select('posts', what='id, title, content, datetime(created) as created, user_id', where='parent = 0',
                      offset=offset, limit=perpage, order='id DESC')
    postcount = db.query("SELECT COUNT(*) AS count FROM posts")[0]
    pages = postcount.count / perpage
    if postcount.count % perpage > 0:
        pages += 1
    for i in posts:
        output += '<tr>'
        user = db.select('users', what='username', where="id = $i.user_id", vars=locals())[0]
        output += '<td style="width: 5%">'
        output += '<a href="#" class="button red">'+list_comment(i.id)+'</a>'
        output += '</td>'
        output += '<td style="width: 70%">'
        output += '<h4><a href="/view/'+str(i.id)+'">'+i.title+'</a></h4>'
        output += '</td>'
        output += ' <td>'
        output += ' <h5><a>'+i.created+'</a></h5>'
        output += ' </td>'
        output += ' <td>'
        output += ' <h5><a>'+user.username+'</a></h5>'
        output += ' </td>'
        output += '</tr>'
    return output, pages


def view_post(page_id):
    page = db.select('posts', what='id, title, content, datetime(created) as created, user_id', where="id = $page_id",
                     vars=locals())[0]
    user = db.select('users', what='username', where="id = $page.user_id", vars=locals())[0]
    return page, user


def new_post(username, password, title, content):
    user_id = register_or_login(username, password)
    if user_id:
        return db.insert('posts', title=title, content=content, user_id=user_id, created=datetime.datetime.utcnow(),
                         parent=0)


def new_comment(username, password, title, content, parent):
    user_id = register_or_login(username, password)
    if user_id:
        return db.insert('posts', title=title, content=content, user_id=user_id, created=datetime.datetime.utcnow(),
                         parent=parent)
    else:
        return 0


def register_or_login(username, password):
    user = db.select('users', what='id', where="username = $username", vars=locals())
    if not user:
        pwdhash = hashlib.md5(password).hexdigest()
        return db.insert('users', username=username, password=pwdhash, created=datetime.datetime.utcnow())
    else:
        if login(username, password):
            return list(user)[0]['id']
        else:
            return 0


def login(username, password):
    pwdhash = hashlib.md5(password).hexdigest()
    return db.where('users', username=username, password=pwdhash)
