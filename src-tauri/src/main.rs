#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            hka_lib::load_config,
            hka_lib::save_config,
            hka_lib::open_link,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
