document.getElementById('uploadButton').addEventListener('click', () => {
  document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', handleImageUpload);

async function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) {
      alert("Please select an image!");
      return;
  }
  displayUploadedImage(file);
  const formData = new FormData();
  formData.append('image', file);

  try {
      console.log('Uploading image...');
      const response = await fetch('/upload', {
          method: 'POST',
          body: formData
      });

      const data = await response.json();
      console.log('Response from server:', data);

      if (data.ingredients) {
          openIngredientsModal(data.ingredients);
      } else {
          alert(data.error || "No ingredients recognized.");
      }
  } catch (error) {
      console.error("Error during image upload:", error);
      alert("An error occurred while uploading the image.");
  }
}
function displayUploadedImage(file) {
  const reader = new FileReader();
  reader.onload = function (e) {
      const imagePreview = document.getElementById('imagePreview');
      imagePreview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" style="max-width: 50%; height: auto; border: 2px solid #ddd; padding: 5px; border-radius: 5px;">`;
  };
  reader.readAsDataURL(file);
}

function openIngredientsModal(ingredients) {
  document.getElementById('recognizedIngredientsList').textContent = ingredients.join(', ');
  document.getElementById('ingredientsModal').style.display = 'block';
  window.recognizedIngredients = ingredients;
}

function closeIngredientsModalAndOpenPreferences() {
  document.getElementById('ingredientsModal').style.display = 'none';
  document.getElementById('preferencesModal').style.display = 'block';
}

function closePreferencesModal() {
  document.getElementById('preferencesModal').style.display = 'none';
}

async function sendToGPT() {
  const preferences = document.getElementById('preferencesInput').value;
  const ingredients = window.recognizedIngredients || [];

  if (!ingredients.length) {
      alert("No ingredients recognized.");
      return;
  }

  closePreferencesModal();  // 关闭偏好设置弹窗

  try {
      console.log('Sending POST request to /generate-recipe...');
      const response = await fetch('/generate-recipe', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ ingredients, preferences })
      });

      const data = await response.json();
      console.log('Generated Recipes:', data);

      let recipes = data.recipes;

      // 如果返回的是字符串而不是数组，拆分成数组
      if (typeof recipes === 'string') {
          recipes = recipes.split('\n\n');
      }

      displayRecipes(recipes);  // 显示生成的菜谱
  } catch (error) {
      console.error("Error during recipe generation:", error);
      alert("An error occurred while generating the recipe.");
  }
}



function displayRecipes(recipes) {
  const modalContent = document.getElementById('modalContent');
  if (!modalContent) {
      console.error('Element with id "modalContent" not found.');
      return;
  }

  // 如果 recipes 是字符串，拆分成数组
  if (typeof recipes === 'string') {
      recipes = recipes.split('\n\n'); // 假设菜谱之间用两个换行符分隔
  }

  // 渲染菜谱内容，每段用 <p> 包裹
  const formattedRecipes = recipes.map(recipe => `<p>${recipe.replace(/\n/g, '<br>')}</p>`).join('');

  // 插入菜谱内容到弹窗
  modalContent.innerHTML = formattedRecipes;

  // 显示生成菜谱弹窗
  openRecipeModal();
}

function openRecipeModal() {
  const modal = document.getElementById('recipeModal');
  if (modal) {
      modal.style.display = 'flex';  // 显示弹窗并居中
  }
}

function closeRecipeModal() {
  const modal = document.getElementById('recipeModal');
  if (modal) {
      modal.style.display = 'none';  // 关闭弹窗
  }
}

function openGeneratedRecipesModal(recipes) {
  const contentElement = document.getElementById('generatedRecipesContent');
  if (contentElement) {
    // 将数组中的每一项用段落包裹起来
    const formattedRecipes = recipes.map(recipe => `<p>${recipe}</p>`).join('');
    contentElement.innerHTML = formattedRecipes; // 更新弹窗内容
    document.getElementById('recognitionResult').style.display = 'block'; // 显示弹窗
  } else {
    console.error('Element with id "generatedRecipesContent" not found.');
  }
}
function openRecipeModal() {
  const modal = document.getElementById('recipeModal');
  if (modal) {
    modal.style.display = 'block';
  }
}

function closeRecipeModal() {
  const modal = document.getElementById('recipeModal');
  if (modal) {
    modal.style.display = 'none';
  }
}


function showActionButtons() {
  const container = document.getElementById('recognitionResult');
  container.innerHTML = `
      <button id="tryAgainButton" onclick="tryAgain()">Try Again</button>
      <button id="likeItButton" onclick="showGutenAppetit()">I Like It</button>
  `;
  container.style.display = 'block';
}



function closeGeneratedRecipesModal() {
  document.getElementById('recognitionResult').style.display = 'none';
}

function tryAgain() {
  closeRecipeModal(); // 关闭弹窗
  sendToGPT(); // 重新请求生成新的菜谱
}

function showGutenAppetit() {
  alert("Guten Appetit! Enjoy your meal!");
  closeRecipeModal(); // 关闭弹窗
}
function closeGutenAppetitModal() {
  document.getElementById('gutenAppetitModal').style.display = 'none';
}
