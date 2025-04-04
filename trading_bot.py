import websocket
import pandas as pd
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import DummyVecEnv
from trading_env import TradingEnv
from stable_baselines3.common.evaluation import evaluate_policy
def on_message(ws, message):
    print(f"Received: {message}")

def on_open(ws):
    ws.send("Hello from Python!")


if __name__ == "__main__":
    # Create a WebSocket connection to the server
    ws = websocket.WebSocketApp("ws://127.0.0.1:8080",
                                on_open=on_open,
                                on_message=on_message)
    ws.run_forever()
    

    # Load your data
    df = pd.read_csv('your_data.csv')
    env = DummyVecEnv([lambda: TradingEnv(df)])
    model = A2C('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save("trading_model")
    


    # Load the trained model
    model = A2C.load("trading_model")
    env = DummyVecEnv([lambda: TradingEnv(df)])
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        print(f"Action: {action}, Reward: {rewards}")
        env.render()
    env.close()
    
    # Evaluate the model
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"Mean reward: {mean_reward}, Std reward: {std_reward}")
    env.close()
    