import React from 'react';
import ModelSelector from './ModelSelector';
import '../styles/SideMenu.css';

const SideMenu = ({ isSideMenuOpen, toggleSideMenu, onModelSelect }) => {
  return (
    <div className={`side-menu ${isSideMenuOpen ? 'open' : 'closed'}`}>
      <button
        className={`fold-button ${isSideMenuOpen ? 'open' : ''}`}
        onClick={toggleSideMenu}
      >
        {/* Arrow content is handled by CSS pseudo-elements */}
      </button>
      {isSideMenuOpen && (
        <div className="side-menu-content">
          <h3>Select Model and LoRA</h3>
          <ModelSelector onModelSelect={onModelSelect} />
        </div>
      )}
    </div>
  );
};

export default SideMenu;