from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Enum as EnumType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import enum, datetime, uuid as puuid


database = SQLAlchemy()

class DeleteStrategy(enum.Enum):
    NEVER = 'NEVER'
    AFTER_DAY = 'AFTER_DAY'
    AFTER_WEEK = 'AFTER_WEEK'
    AFTER_MONTH = 'AFTER_MONTH'

    def get_strategy_by_name(name):
        for strategy in DeleteStrategy:
            if strategy.name == name:
                return strategy
        
        return None

DeleteStrategyType = EnumType(DeleteStrategy, name='delete_strategy')

class Snippet(database.Model):
    __tablename__ = 'snippets'
    
    uuid: Mapped[puuid.UUID] = mapped_column(UUID(), primary_key=True, default=puuid.uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), default=datetime.datetime.now)
    title: Mapped[str] = mapped_column(String(128))
    content: Mapped[str] = mapped_column(String())
    views_count: Mapped[int] = mapped_column(Integer(), default=0)
    duuid: Mapped[puuid.UUID] = mapped_column(UUID(), unique=True, index=True, default=puuid.uuid4)
    dstrategy: Mapped[DeleteStrategy] = mapped_column(DeleteStrategyType)

    def __init__(self, title, content, dstrategy):
        super().__init__()
        self.title = title
        self.content = content
        self.dstrategy = dstrategy
    
    def __repr__(self):
        return f'<Snippet {self.uuid}>'

    def short_creation_date(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M')