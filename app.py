from flask import Flask, request, render_template, redirect, abort
import json
from models import database, Snippet, DeleteStrategy


app = Flask(__name__)
app.config.from_file('config.json', json.load)

database.init_app(app)

@app.get('/')
def index():
    return redirect('/snippets/create')

@app.route('/snippets/create', methods=['GET', 'POST'])
def create_snippet():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        dstrategy_name = request.form.get('dstrategy')
        
        dstrategy = None
        for strategy in DeleteStrategy:
            if strategy.name == dstrategy_name:
                dstrategy = strategy
                break
        
        if dstrategy is None:
            abort(400)

        snippet = Snippet(title, content, dstrategy)
        database.session.add(snippet)
        database.session.commit()

        return render_template(
            'snippet_links.html', 
            snippet_title=snippet.title,
            creation_date=snippet.created_at,
            view_url=f'{request.url_root}snippets/{snippet.uuid}',
            delete_url=f'{request.url_root}snippets/d/{snippet.duuid}'
        )
    return render_template('snippet_create.html')

@app.get('/snippets/<uuid>')
def view_snippet(uuid):
    snippet = database.session.query(Snippet).where(Snippet.uuid == uuid).scalar()
    if snippet is None:
        abort(404)
    
    return render_template(
        'snippet_view.html',
        snippet_title=snippet.title,
        snippet_content=snippet.content,
        created_at=snippet.short_creation_date(),
        show_delete_form=False
    )

@app.route('/snippets/d/<duuid>', methods=['GET', 'POST'])
def delete_snippet(duuid):
    snippet = database.session.query(Snippet).where(Snippet.duuid == duuid).scalar()
    if snippet is None:
            abort(404)

    if request.method == 'POST': 
        database.session.delete(snippet)
        database.session.commit()

        return 'DELETED', 204
    
    return render_template(
        'snippet_view.html',
        snippet_title=snippet.title,
        snippet_content=snippet.content,
        created_at=snippet.short_creation_date(),
        show_delete_form=True
    )

if __name__ == '__main__':
    with app.app_context():
        database.create_all()
    
    app.run(debug=True)