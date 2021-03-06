#!env python2
import click
import sqlite3 as lite
import sys
import textwrap as tw
from signal import signal, SIGPIPE, SIG_DFL
from texttable import Texttable
import os
import pkg_resources

@click.command()
@click.option("--skill", "-s", is_flag=True, help="Search skills and inducements")
@click.option("--roster", "-r", is_flag=True, help="Search rosters")
# @click.option("--inducement", "-i", is_flag=True)
@click.option("--star", "-p", is_flag=True, help="Search star players")
# @click.option("--searchall", "-a", default=True, is_flag=True, help="Do stuff")
@click.option("--deepsearch", '-d', default=False, is_flag=True, help="Include rules text in search")
@click.argument("searchterm", required=True)
def cli(searchterm, deepsearch, roster, star, skill):
    """
    Quickly checks a Blood Bowl rule. Searches all rule types by default.
    """

    searchall = True
    signal(SIGPIPE,SIG_DFL) 
    search_db(searchterm, searchall=searchall, skill=skill, roster=roster, star=star,
            deepsearch=deepsearch)

def search_rules(con, searchterm, deepsearch, return_rows=False, exact=False):
    cur = con.cursor()
    like = '%' + searchterm + '%'
    bindings = [like]
    sql = "SELECT * FROM rules where name like ?"

    if exact:
        sql = "SELECT * FROM rules WHERE name = ? COLLATE NOCASE"
        bindings = [searchterm]

    # sql = "SELECT * FROM rules where name like '%" + searchterm + "%'"
    if deepsearch:
        sql += " or rules like ?"
        bindings.append(like)

    cur.execute(sql, bindings)
    
    rows = cur.fetchall()
    wrap = tw.TextWrapper(width=80)
    output = ""
    if return_rows:
        return rows

    for row in rows:
        if len(row[3]) > 0:
            header = "%s (%s)" % (row[0], row[3])
        else:
            header = row[0]
        output += header + "\n"
        output += "-" * len(header) + "\n"
        output += tw.fill(row[1])
        output += "\n\n"

    return output

def search_roster(con, searchterm, deepsearch, return_rows=False):
    cur = con.cursor()
    like = '%' + searchterm + '%'
    bindings = [like, like]
    sql = "SELECT * FROM roster where position like ? or race like ?"
    if deepsearch:
        sql += " or skills like ?"
        bindings.append(like)

    cur.execute(sql, bindings)
    rows = cur.fetchall()
    if return_rows:
        return rows
    wrap = tw.TextWrapper(width=80)

    headers = ['Race', '#', 'Position', 'MV', 'ST', 'AG', 'AV', 'Cost', 'Skills', 'Norm', 'Dbles']
    out = [headers]
    for row in rows:
        out.append([row[0], row[2], row[1], 
            str(row[5]) if row[5] else "",
            str(row[6]) if row[6] else "",
            str(row[7]) if row[7] else "",
            str(row[8]) if row[8] else "",
            row[3], row[4],
            row[9], row[10]])
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_width([11, 4, 12, 2, 2, 2, 2, 4, 15, 5, 5])

    table.add_rows(out)

    if len(rows) > 0:
        return table.draw() + "\n"

    return ""
        # click.echo(table.draw() + "\n")

def search_sp(con, searchterm, deepsearch, return_rows=False):
    cur = con.cursor()
    like = '%' + searchterm + '%'
    bindings = [like, like]
    sql = "SELECT * FROM starplayer where name like ? or races like ?"
    if deepsearch:
        sql += " or skills like ?"
        bindings.append(like)

    cur.execute(sql, bindings)
    rows = cur.fetchall()

    if return_rows:
        return rows

    wrap = tw.TextWrapper(width=80)

    headers = ['Name', 'Races', 'Price', 'MA', 'ST', 'AG', 'AV', 'Skills']
    out = [headers]
    for row in rows:
        out.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
    table = Texttable()
    table.set_deco(Texttable.HEADER)

    table.set_deco(Texttable.HEADER)
    table.set_cols_width([25, 18, 5, 2, 2, 2, 2, 25])
    table.add_rows(out)


    if len(rows) > 0:
        return table.draw() + "\n"
    return ""

def search_db(searchterm, blobtype=None, searchall=True, deepsearch=False, 
        roster=False, star=False, skill=False):

    if skill or star or roster:
        searchall = False
    datafile = pkg_resources.resource_filename(__name__, "crp") + "/crp.db"

    with lite.connect(datafile) as con:
        cur = con.cursor()  

        if searchall or skill:
            click.echo(search_rules(con, searchterm, deepsearch))
        if searchall or roster:
            click.echo(search_roster(con, searchterm, deepsearch))
        if searchall or star:
            click.echo(search_sp(con, searchterm, deepsearch))

def get_connection():
    datafile = pkg_resources.resource_filename(__name__, "crp") + "/crp.db"
    return lite.connect(datafile)
