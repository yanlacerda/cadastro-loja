from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Numeric, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base para criar as classes como tabelas do banco de dados
Base = declarative_base()


# ============ MODELS ============

class Cliente(Base):  # Model que representa o Cliente
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False)
    telefone = Column(String(15), nullable=False)

    # Relacionamento: um cliente pode ter muitos pedidos
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ClienteID={self.id}, Nome={self.nome!r}, Email={self.email!r}>"

    
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome_produto = Column(String(160), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint("preco >= 0", name="ck_produto_preco"),
        CheckConstraint("estoque >= 0", name="ck_produto_estoque"),
    )
    itens = relationship("PedidoItem", back_populates="produto")

    def __repr__(self):
        return f"<Produto id={self.id}, nome_produto={self.nome_produto!r}, preco={self.preco}, Estoque={self.estoque}>"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    data_pedido = Column(DateTime, default=datetime.utcnow, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    preco_total = Column(Numeric(10, 2), nullable=False)
    #status = Column(String(120),nullable=False, default="Aberto")

    cliente = relationship("Cliente", back_populates="pedidos")
    itens = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")

    #def total(self):
        #return sum((it.quantidade * it.preco_unitario) for it in self.itens)

    def __repr__(self):
        return f"<Pedido id={self.id}, ClienteID={self.cliente_id}, Preço Total={self.preco_total}, Data={self.data_pedido}>"

    
class PedidoItem(Base):
    __tablename__ = "pedido_items"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    #__table_args__ ={
    #    CheckConstraint("quantidade>0",name="ck_item_quantidade"),
    #    CheckConstraint("preco_unitario >=0",name="ck_item_preco"),
    #}

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

    def __repr__(self):
        return f"<PedidoItem id={self.id}, PedidoID={self.pedido_id}, ProdutoID={self.produto_id}, Quantidade={self.quantidade}, PreçoUnitário={self.preco_unitario}>"
    
    def get_engine(db_url: str = "sqlite:///loja_jogos.db"):
        return create_engine(db_url, echo=False, future=True)
    
    def create_session(db_url: str = "sqlite:///loja_jogos.db"):
        engine = get_engine(db_url)
        Base.metadata.create_all(engine)
        SessionLocal= sessionmaker(bind=engine, autoflush=False, autocomit=False, future=True)
        return SessionLocal()