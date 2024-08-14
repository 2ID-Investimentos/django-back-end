import sqlite3
import random

# Caminho para o banco de dados SQLite
db_path = "db.sqlite3"  # Altere este caminho conforme necessário

# Conectando ao banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Selecionando todos os usuários e ativos
cursor.execute("SELECT id FROM database_user;")
users = cursor.fetchall()

cursor.execute("SELECT id, current_price FROM database_stock;")
stocks = cursor.fetchall()


# Função para gerar transações aleatórias
def create_transactions():
    transactions = []
    for user in users:
        user_id = user[0]
        num_transactions = random.randint(5, 10)

        for _ in range(num_transactions):
            stock_id, current_price = random.choice(stocks)
            amount = random.randint(1, 100)
            unitary_value = current_price
            total_value = amount * unitary_value

            # Data aleatória
            year = random.randint(2020, 2024)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date = f"{year}-{month:02d}-{day:02d}"

            # Escolhe aleatoriamente entre compra e venda
            if random.choice(["buy", "sell"]) == "buy":
                transactions.append(
                    ("buy", date, amount, unitary_value, total_value, stock_id, user_id)
                )
            else:
                transactions.append(
                    (
                        "sell",
                        date,
                        amount,
                        unitary_value,
                        total_value,
                        stock_id,
                        user_id,
                    )
                )
    return transactions


# Gerando as transações
transactions = create_transactions()

# Inserindo as transações no banco de dados
for transaction in transactions:
    table, date, amount, unitary_value, total_value, stock_id, user_id = transaction
    if table == "buy":
        cursor.execute(
            """
            INSERT INTO database_buy (date, amount, unitary_value, total_value, ticker_id, user_id)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
            (date, amount, unitary_value, total_value, stock_id, user_id),
        )
    else:
        cursor.execute(
            """
            INSERT INTO database_sell (date, amount, unitary_value, total_value, ticker_id, user_id)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
            (date, amount, unitary_value, total_value, stock_id, user_id),
        )

# Salvando as alterações
conn.commit()

# Fechando a conexão
conn.close()
