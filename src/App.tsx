import { useState, useEffect, useCallback } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-shell";

interface ButtonConfig {
  name: string;
  link: string;
}

type Config = Record<string, ButtonConfig>;

interface EditDialogProps {
  initial: ButtonConfig;
  onSave: (data: ButtonConfig) => void;
  onClear: () => void;
  onCancel: () => void;
}

function EditDialog({ initial, onSave, onClear, onCancel }: EditDialogProps) {
  const [name, setName] = useState(initial.name);
  const [link, setLink] = useState(initial.link);

  return (
    <div className="dialog-overlay" onClick={onCancel}>
      <div className="dialog" onClick={(e) => e.stopPropagation()}>
        <h3>Edit Button</h3>
        <div className="dialog-field">
          <label>Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Button label"
            autoFocus
          />
        </div>
        <div className="dialog-field">
          <label>Link</label>
          <input
            value={link}
            onChange={(e) => setLink(e.target.value)}
            placeholder="https://..."
          />
        </div>
        <div className="dialog-buttons">
          <button className="btn-save" onClick={() => onSave({ name, link })}>
            Save
          </button>
          <button className="btn-clear" onClick={onClear}>
            Clear
          </button>
          <button className="btn-cancel" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [config, setConfig] = useState<Config>({});
  const [editKey, setEditKey] = useState<string | null>(null);

  const loadConfig = useCallback(async () => {
    try {
      const cfg = await invoke<Config>("load_config");
      setConfig(cfg);
    } catch (err) {
      console.error("Failed to load config:", err);
    }
  }, []);

  useEffect(() => {
    loadConfig();
  }, [loadConfig]);

  const handleSaveConfig = async (cfg: Config) => {
    try {
      await invoke("save_config", { config: cfg });
      setConfig(cfg);
    } catch (err) {
      console.error("Failed to save config:", err);
    }
  };

  const handleCellClick = async (key: string) => {
    const entry = config[key];
    if (entry?.link) {
      try {
        await open(entry.link);
      } catch (err) {
        console.error("Failed to open link:", err);
      }
    } else {
      setEditKey(key);
    }
  };

  const handleSave = (data: ButtonConfig) => {
    const trimmed = {
      name: data.name.trim(),
      link: data.link.trim(),
    };
    const newConfig = { ...config };
    if (trimmed.name || trimmed.link) {
      newConfig[editKey!] = trimmed;
    } else {
      delete newConfig[editKey!];
    }
    handleSaveConfig(newConfig);
    setEditKey(null);
  };

  const handleClear = () => {
    const newConfig = { ...config };
    delete newConfig[editKey!];
    handleSaveConfig(newConfig);
    setEditKey(null);
  };

  const cells = Array.from({ length: 25 }, (_, i) => String(i));
  const editData = editKey ? config[editKey] || { name: "", link: "" } : { name: "", link: "" };

  return (
    <div className="app">
      <div className="title">HKA - Hyperlink Keyboard App</div>
      <div className="grid">
        {cells.map((key) => {
          const entry = config[key];
          const hasContent = entry?.name;
          return (
            <div
              key={key}
              className={`cell ${hasContent ? "" : "empty"}`}
              onClick={() => handleCellClick(key)}
            >
              {hasContent ? entry.name : "+"}
            </div>
          );
        })}
      </div>
      {editKey !== null && (
        <EditDialog
          initial={editData}
          onSave={handleSave}
          onClear={handleClear}
          onCancel={() => setEditKey(null)}
        />
      )}
    </div>
  );
}
