# Импорт необходимых библиотек
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report



# Предполагается, что файл называется 'winequality-red.csv'
data = pd.read_csv('winequality-red.csv', sep=',')

# Создание бинарного столбца для классификации
data['quality_binary'] = data['quality'].apply(lambda x: 1 if x >= 7 else 0)

# Разделение данных на признаки и целевую переменную
X = data.drop(['quality', 'quality_binary'], axis=1)
Y = data['quality_binary']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Обучение модели логистической регрессии
model = LogisticRegression(max_iter=10000)
model.fit(X_train, Y_train)

# Предсказание и оценка модели
Y_pred = model.predict(X_test)
report = classification_report(Y_test, Y_pred)

# Вывод уравнения гиперповерхности
coefficients = model.coef_[0]
intercept = model.intercept_[0]

print("Коэффициенты:", coefficients)
print("Свободный член:", intercept)
print("Отчет о классификации:\n", report)