from database import engine
import models

def create_tables():
    models.Base.metadata.create_all(bind=engine)
    print("테이블이 성공적으로 생성되었습니다!")

if __name__ == "__main__":
    create_tables() 