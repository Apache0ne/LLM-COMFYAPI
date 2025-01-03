import React, { useState, useEffect, useCallback } from 'react';
import { getCategories, getModelsAndLoras } from '../api/api';
import '../styles/ModelSelector.css';

function ModelSelector({ onModelSelect }) {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [models, setModels] = useState([]);
  const [loras, setLoras] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedLora, setSelectedLora] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchCategories = useCallback(async () => {
    setIsLoading(true);
    setError('');
    try {
      const fetchedCategories = await getCategories();
      setCategories(fetchedCategories);
    } catch (error) {
      setError('Failed to fetch categories');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchModelsAndLoras = useCallback(async () => {
    if (!selectedCategory) return;
    setIsLoading(true);
    setError('');
    try {
      const { models: fetchedModels, loras: fetchedLoras } = await getModelsAndLoras(selectedCategory);
      setModels(fetchedModels);
      setLoras(fetchedLoras);
    } catch (error) {
      setError('Failed to fetch models and LoRAs');
    } finally {
      setIsLoading(false);
    }
  }, [selectedCategory]);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  useEffect(() => {
    fetchModelsAndLoras();
  }, [fetchModelsAndLoras]);

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
    setSelectedModel('');
    setSelectedLora('');
  };

  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
    onModelSelect({
      category: selectedCategory,
      model: e.target.value,
      lora: selectedLora
    });
  };

  const handleLoraChange = (e) => {
    setSelectedLora(e.target.value);
    onModelSelect({
      category: selectedCategory,
      model: selectedModel,
      lora: e.target.value
    });
  };

  if (isLoading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="model-selector">
      <select
        value={selectedCategory}
        onChange={handleCategoryChange}
        disabled={isLoading}
        className="model-selector-select"
      >
        <option value="">Select a category</option>
        {categories.map((category) => (
          <option key={category} value={category}>{category}</option>
        ))}
      </select>

      <select
        value={selectedModel}
        onChange={handleModelChange}
        disabled={!selectedCategory || isLoading}
        className="model-selector-select"
      >
        <option value="">Select a model</option>
        {models.map((model) => (
          <option key={model} value={model}>{model}</option>
        ))}
      </select>

      <select
        value={selectedLora}
        onChange={handleLoraChange}
        disabled={!selectedModel || isLoading}
        className="model-selector-select"
      >
        <option value="">Select a LoRA (optional)</option>
        {loras.map((lora) => (
          <option key={lora} value={lora}>{lora}</option>
        ))}
      </select>
    </div>
  );
}

export default ModelSelector;