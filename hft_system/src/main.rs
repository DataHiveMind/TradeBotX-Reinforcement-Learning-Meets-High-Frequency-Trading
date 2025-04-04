use tokio::net::TcpListener;
use tokio::stream::StreamExt;
use tokio_tungstenite::accept_async;
use tokio_tungstenite::tungstenite::protocol::Message;

#[tokio::main]
async fn main() {
    let addr = "127.0.0.1:8080".to_string();
    let listener = TcpListener::bind(&addr).await.unwrap();
    while let Some(stream) = listener.incoming().next().await {
        let stream = stream.unwrap();
        tokio::spawn(async move {
            let ws_stream = accept_async(stream).await.unwrap();
            let (write, read) = ws_stream.split();
            read.for_each(|message| async {
                let message = message.unwrap();
                if message.is_text() || message.is_binary() {
                    write.send(Message::Text("Hello from Rust!".into())).await.unwrap();
                }
            }).await;
        });
    }
}