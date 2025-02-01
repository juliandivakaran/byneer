import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Load the trained model
model = load_model('C:/Users/user/Pictures/lpd/lstm_model.h5')  # Update path as needed

# Load your test data (assuming `df` is the DataFrame)
# Replace with actual data loading logic, for example:
# df = pd.read_csv('your_test_data.csv')

# For example, let's assume the `df` is already available:
df = pd.DataFrame({
    'feature1': np.random.rand(100),
    'feature2': np.random.rand(100),
    'sequence': np.random.randint(1, 100, size=100),
})

# Handle NaN and infinity values in the DataFrame
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# Keep only numeric columns
df = df.select_dtypes(include=[np.number])

# Define Features (X) and Target (y)
X = df.drop(columns=['sequence']).values  # Features
y = df['sequence'].values.reshape(-1, 1)  # Target

# Scale Features and Target
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

# Define Time Steps for LSTM (e.g., last 3 records predict the next)
timesteps = 3
X_series, y_series = [], []

for i in range(len(X_scaled) - timesteps):
    X_series.append(X_scaled[i:i + timesteps])  # Last `timesteps` data points
    y_series.append(y_scaled[i + timesteps])  # Next value

X_series, y_series = np.array(X_series), np.array(y_series)

# Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X_series, y_series, test_size=0.2, shuffle=False)

# Predict on Test Data
y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled)  # Convert back

# Evaluate the Model
mse = np.mean((y_pred - scaler_y.inverse_transform(y_test.reshape(-1, 1)))**2)
print(f"Mean Squared Error on Test Set: {mse}")

# Predict the Next Number in Sequence
latest_data = X_scaled[-timesteps:].reshape(1, timesteps, X.shape[1])  # Last sequence
next_number_scaled = model.predict(latest_data)
next_number = scaler_y.inverse_transform(next_number_scaled.reshape(-1, 1))[0][0]

print(f"Predicted Next Number in Sequence: {next_number}")
