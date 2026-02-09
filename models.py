from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Enum as EnumType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import enum, datetime, uuid as puuid

database = SQLAlchemy()

class DeleteStrategy(enum.Enum):
    NEVER = None
    AFTER_HOUR = datetime.timedelta(hours=1)
    AFTER_DAY = datetime.timedelta(days=1)
    AFTER_WEEK = datetime.timedelta(weeks=1)
    AFTER_MONTH = datetime.timedelta(days=31)

    @staticmethod
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
    delete_at: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=True)

    def __init__(self, title, content, dstrategy):
        super().__init__()
        self.title = title
        self.content = content
        self.dstrategy = dstrategy
        
        if dstrategy.value is not None:
            self.delete_at = datetime.datetime.now() + dstrategy.value
    
    def __repr__(self):
        return f'<Snippet {self.uuid}>'

    def short_creation_date(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M')