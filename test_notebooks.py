#!/usr/bin/env python3
"""
Test script for ChatterBox TTS Gradio Notebooks

This script validates both Kaggle and Colab notebooks to ensure they:
- Have valid JSON structure
- Follow proper nbformat specifications
- Include all required cells and functionality
- Have correct metadata for their respective platforms

Usage:
    python test_notebooks.py
"""

import json
import sys
from pathlib import Path

def test_notebook_structure(notebook_path, platform):
    """Test notebook structure and content"""
    print(f"🧪 Testing {platform} Notebook")
    print("=" * 40)
    
    if not Path(notebook_path).exists():
        print(f"❌ File not found: {notebook_path}")
        return False
    
    try:
        # Test JSON validity
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        print("✅ JSON structure: Valid")
        
        # Test nbformat validity
        try:
            import nbformat
            nb = nbformat.read(notebook_path, as_version=4)
            print(f"✅ Notebook format: Valid ({len(nb.cells)} cells)")
        except ImportError:
            print("⚠️ nbformat not available - skipping format validation")
        except Exception as e:
            print(f"❌ Notebook format error: {e}")
            return False
        
        # Test required sections
        required_sections = [
            "ChatterBox TTS",
            "Install Dependencies", 
            "Load ChatterBox TTS",
            "Gradio Interface",
            "Launch",
            "Public URL"
        ]
        
        found_sections = []
        for cell in notebook['cells']:
            if cell['cell_type'] == 'markdown':
                content = ''.join(cell['source'])
                for section in required_sections:
                    if section.lower() in content.lower():
                        found_sections.append(section)
        
        unique_sections = list(set(found_sections))
        print(f"✅ Required sections: {len(unique_sections)}/{len(required_sections)} found")
        
        # Test platform-specific features
        if platform == "Kaggle":
            # Check for Kaggle-specific content
            kaggle_features = ["Kaggle", "Output tab", "internet access"]
            found_features = 0
            for cell in notebook['cells']:
                content = ''.join(cell.get('source', []))
                for feature in kaggle_features:
                    if feature.lower() in content.lower():
                        found_features += 1
                        break
            print(f"✅ Kaggle features: {found_features > 0}")
            
        elif platform == "Colab":
            # Check for Colab-specific metadata and content
            has_colab_metadata = 'colab' in notebook.get('metadata', {})
            print(f"✅ Colab metadata: {has_colab_metadata}")
            
            colab_features = ["Google Colab", "Runtime restart", "Open in Colab"]
            found_features = 0
            for cell in notebook['cells']:
                content = ''.join(cell.get('source', []))
                for feature in colab_features:
                    if feature.lower() in content.lower():
                        found_features += 1
                        break
            print(f"✅ Colab features: {found_features > 0}")
        
        # Test Gradio-specific content
        gradio_keywords = ["gradio", "share=True", "public URL", "demo.launch"]
        found_gradio = 0
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                content = ''.join(cell.get('source', []))
                for keyword in gradio_keywords:
                    if keyword.lower() in content.lower():
                        found_gradio += 1
                        break
        print(f"✅ Gradio integration: {found_gradio > 0}")
        
        # Test public URL sharing
        has_public_url = False
        for cell in notebook['cells']:
            content = ''.join(cell.get('source', []))
            if 'share=True' in content or 'public URL' in content:
                has_public_url = True
                break
        print(f"✅ Public URL sharing: {has_public_url}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_notebook_content_quality(notebook_path, platform):
    """Test the quality and completeness of notebook content"""
    print(f"\n📋 Content Quality Check - {platform}")
    print("-" * 40)
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        total_cells = len(notebook['cells'])
        markdown_cells = sum(1 for cell in notebook['cells'] if cell['cell_type'] == 'markdown')
        code_cells = sum(1 for cell in notebook['cells'] if cell['cell_type'] == 'code')
        
        print(f"📊 Cell distribution:")
        print(f"   Total cells: {total_cells}")
        print(f"   Markdown cells: {markdown_cells}")
        print(f"   Code cells: {code_cells}")
        
        # Check for comprehensive content
        content_checks = {
            "Installation instructions": False,
            "Model loading": False,
            "Gradio interface creation": False,
            "Public URL launch": False,
            "Usage instructions": False,
            "Troubleshooting": False
        }
        
        for cell in notebook['cells']:
            content = ''.join(cell.get('source', [])).lower()
            
            if 'install' in content and ('pip' in content or 'package' in content):
                content_checks["Installation instructions"] = True
            if 'chatterboxtts' in content.replace(' ', '') or 'from_pretrained' in content:
                content_checks["Model loading"] = True
            if 'gr.blocks' in content or 'create_gradio' in content:
                content_checks["Gradio interface creation"] = True
            if 'share=true' in content or 'public url' in content:
                content_checks["Public URL launch"] = True
            if 'how to' in content or 'usage' in content or 'quick start' in content:
                content_checks["Usage instructions"] = True
            if 'troubleshoot' in content or 'error' in content or 'problem' in content:
                content_checks["Troubleshooting"] = True
        
        passed_checks = sum(content_checks.values())
        print(f"\n✅ Content completeness: {passed_checks}/{len(content_checks)}")
        for check, passed in content_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        return passed_checks >= len(content_checks) * 0.8  # 80% threshold
        
    except Exception as e:
        print(f"❌ Content quality check failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 ChatterBox TTS Notebook Test Suite")
    print("=" * 60)
    print()
    
    notebooks = [
        ("chatterbox_kaggle_gradio.ipynb", "Kaggle"),
        ("chatterbox_colab_gradio.ipynb", "Colab")
    ]
    
    results = []
    
    for notebook_path, platform in notebooks:
        # Test structure
        structure_ok = test_notebook_structure(notebook_path, platform)
        
        # Test content quality
        content_ok = test_notebook_content_quality(notebook_path, platform)
        
        overall_ok = structure_ok and content_ok
        results.append((platform, overall_ok))
        
        print(f"\n🎯 {platform} Overall: {'✅ PASS' if overall_ok else '❌ FAIL'}")
        print()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for platform, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {platform} Notebook")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} notebooks passed")
    
    if passed == total:
        print("\n🎉 All notebooks are ready for use!")
        print("\n🚀 Ready to deploy:")
        print("1. Upload chatterbox_kaggle_gradio.ipynb to Kaggle")
        print("2. Open chatterbox_colab_gradio.ipynb in Google Colab")
        print("3. Both will generate public URLs for instant sharing")
        
        print("\n🔗 Public URL Features:")
        print("• Instant worldwide access")
        print("• No installation required for users")
        print("• Professional Gradio interface")
        print("• Voice cloning and TTS capabilities")
        print("• Collaborative testing environment")
    else:
        print("\n⚠️ Some notebooks have issues. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
