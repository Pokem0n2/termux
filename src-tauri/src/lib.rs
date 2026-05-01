use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;

#[derive(Debug, Serialize, Deserialize, Default)]
pub struct ButtonConfig {
    pub name: String,
    pub link: String,
}

pub type Config = HashMap<String, ButtonConfig>;

fn get_config_path() -> PathBuf {
    let exe_dir = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_else(|| PathBuf::from("."));
    exe_dir.join("hka-config.json")
}

#[tauri::command]
fn load_config() -> Result<Config, String> {
    let path = get_config_path();
    if path.exists() {
        let content = fs::read_to_string(&path).map_err(|e| e.to_string())?;
        serde_json::from_str(&content).map_err(|e| e.to_string())
    } else {
        Ok(Config::default())
    }
}

#[tauri::command]
fn save_config(config: Config) -> Result<(), String> {
    let path = get_config_path();
    let content = serde_json::to_string_pretty(&config).map_err(|e| e.to_string())?;
    fs::write(&path, content).map_err(|e| e.to_string())
}

#[tauri::command]
fn open_link(url: String) -> Result<(), String> {
    open::that(&url).map_err(|e| e.to_string())
}
