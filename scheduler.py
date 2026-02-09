from flask_apscheduler import APScheduler

scheduler = APScheduler()

@scheduler.task('interval', id='delete_expired_snippets', seconds=60)
def delete_expired_snippets():
    from datetime import datetime
    from models import database, Snippet
    
    with scheduler.app.app_context():
        expired = Snippet.query.filter(
            Snippet.delete_at.isnot(None),
            Snippet.delete_at <= datetime.now()
        ).all()
        
        for snippet in expired:
            database.session.delete(snippet)
        
        database.session.commit()