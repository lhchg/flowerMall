# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class AppErrorLog(db.Model):
    __tablename__ = 'app_error_log'

    id = db.Column(db.Integer, primary_key=True)
    referer_url = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='当前访问的refer')
    target_url = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue(), info='访问的url')
    query_params = db.Column(db.Text(collation='utf8mb4_0900_ai_ci'), nullable=False, info='get和post参数')
    content = db.Column(db.String(collation='utf8mb4_0900_ai_ci'), nullable=False, info='日志内容')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')
