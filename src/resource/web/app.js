const state = {
  userId: 0,
  articles: [],
  sentences: [],
  selectedArticleId: null,
  currentSentenceId: null,
  sentencePage: 1,
  firstSentencePage: 1,
  lastSentencePage: 0,
  sentencePageSize: 30,
  sentenceTotal: 0,
  isLoadingSentences: false,
  translationStatus: {},
  currentHistoryItems: [],
  activeHistoryId: null,
  isSubmittingReview: false,
  isGeneratingLlm: false,
  isUploadingArticle: false,
  llmTranslation: null,
  lastReview: null,
};

const els = {
  articleSelect: document.querySelector("#articleSelect"),
  jumpSentenceForm: document.querySelector("#jumpSentenceForm"),
  jumpSentenceInput: document.querySelector("#jumpSentenceInput"),
  sentenceList: document.querySelector("#sentenceList"),
  historyList: document.querySelector("#historyList"),
  sourceText: document.querySelector("#sourceText"),
  llmTranslationText: document.querySelector("#llmTranslationText"),
  userTranslationInput: document.querySelector("#userTranslationInput"),
  scoreText: document.querySelector("#scoreText"),
  commentText: document.querySelector("#commentText"),
  sentencePosition: document.querySelector("#sentencePosition"),
  createLlmButton: document.querySelector("#createLlmButton"),
  submitReviewButton: document.querySelector("#submitReviewButton"),
  toast: document.querySelector("#toast"),
  uploadDialog: document.querySelector("#uploadDialog"),
  uploadForm: document.querySelector("#uploadForm"),
  uploadSubmitButton: document.querySelector("#uploadSubmitButton"),
};

function toast(message, type = "info") {
  els.toast.textContent = message;
  els.toast.classList.toggle("error", type === "error");
  els.toast.hidden = false;
  window.clearTimeout(toast.timer);
  toast.timer = window.setTimeout(() => {
    els.toast.hidden = true;
  }, 3200);
}

function setCreateLlmButtonLabel(isLoading = false) {
  els.createLlmButton.innerHTML = isLoading
    ? '<span>生成中</span><kbd>Ctrl + Shift + Enter</kbd>'
    : '<span>生成 AI 翻译</span><kbd>Ctrl + Shift + Enter</kbd>';
}

function setSubmitReviewButtonLabel(isLoading = false) {
  els.submitReviewButton.innerHTML = isLoading
    ? '<span>点评中</span><kbd>Ctrl + Enter</kbd>'
    : '<span>提交点评</span><kbd>Ctrl + Enter</kbd>';
}

async function api(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(payload?.message || `HTTP ${response.status}`);
  }
  if (payload?.code !== 20000) {
    throw new Error(payload?.message || "接口返回失败");
  }
  return payload.data;
}

function currentSentence() {
  return state.sentences.find((sentence) => sentence.id === state.currentSentenceId) || null;
}

function sentencePageForIndex(sentenceIndex) {
  return Math.ceil(sentenceIndex / state.sentencePageSize);
}

function mergeSentences(items) {
  const sentenceMap = new Map(
    state.sentences.map((sentence) => [sentence.id, sentence]),
  );
  items.forEach((sentence) => {
    sentenceMap.set(sentence.id, sentence);
  });
  state.sentences = Array.from(sentenceMap.values()).sort(
    (a, b) => a.sentence_index - b.sentence_index,
  );
}

function sentenceContextWindow(sentence) {
  if (!sentence) {
    return [];
  }

  const startIndex = Math.max(1, sentence.sentence_index - 5);
  const endIndex =
    state.sentenceTotal > 0
      ? Math.min(state.sentenceTotal, sentence.sentence_index + 5)
      : sentence.sentence_index + 5;

  return state.sentences
    .filter(
      (item) =>
        item.sentence_index >= startIndex && item.sentence_index <= endIndex,
    )
    .sort((a, b) => a.sentence_index - b.sentence_index);
}

function renderSourceText(sentence) {
  if (!sentence) {
    els.sourceText.textContent = "请选择左侧句子";
    return;
  }

  els.sourceText.innerHTML = sentenceContextWindow(sentence)
    .map(
      (item) =>
        `<p class="source-sentence ${item.id === sentence.id ? "current" : ""}"><span class="source-sentence-index">#${item.sentence_index}</span><span class="source-sentence-content">${escapeHtml(item.sentence_content)}</span></p>`,
    )
    .join("");
}

function basename(path) {
  return String(path || "").split(/[\\/]/).filter(Boolean).pop() || "";
}

function articleName(article, index) {
  const filename = String(article.filename || basename(article.file_path)).trim();
  if (!filename) {
    return `文章${index + 1}`;
  }
  return filename.length > 28 ? `${filename.slice(0, 28)}...` : filename;
}

function renderArticleSelect() {
  if (!state.articles.length) {
    els.articleSelect.innerHTML = '<option value="">暂无文章</option>';
    els.articleSelect.disabled = true;
    return;
  }

  els.articleSelect.disabled = false;
  els.articleSelect.innerHTML = state.articles
    .map(
      (article, index) => `
        <option value="${article.id}" title="${escapeAttribute(articleName(article, index))}" ${article.id === state.selectedArticleId ? "selected" : ""}>
          ${escapeHtml(articleName(article, index))}
        </option>
      `,
    )
    .join("");
}

function renderSentenceList({ preserveScroll = true } = {}) {
  const scrollTop = preserveScroll ? els.sentenceList.scrollTop : 0;

  if (!state.sentences.length) {
    els.sentenceList.innerHTML = '<div class="empty-state">暂无句子</div>';
    els.sentenceList.scrollTop = scrollTop;
    return;
  }

  const rows = state.sentences
    .map((sentence) => {
      const isTranslated = Boolean(state.translationStatus[sentence.id]);
      return `
        <button class="sentence-card ${sentence.id === state.currentSentenceId ? "active" : ""}"
          data-sentence-id="${sentence.id}" type="button"
          title="${escapeAttribute(sentence.sentence_content)}">
          <span class="sentence-index ${isTranslated ? "translated" : "untranslated"}">#${sentence.sentence_index}</span>
          <span class="sentence-preview">${escapeHtml(sentence.sentence_content)}</span>
        </button>
      `;
    })
    .join("");

  const loading = state.isLoadingSentences
    ? '<div class="list-status">加载中...</div>'
    : "";
  const done =
    state.sentenceTotal > 0 && state.sentences.length >= state.sentenceTotal
      ? '<div class="list-status">已加载全部句子</div>'
      : "";

  els.sentenceList.innerHTML = `${rows}${loading || done}`;
  els.sentenceList.scrollTop = scrollTop;
}

function updateActiveSentenceCard() {
  els.sentenceList.querySelectorAll(".sentence-card").forEach((card) => {
    card.classList.toggle(
      "active",
      Number(card.dataset.sentenceId) === state.currentSentenceId,
    );
  });
}

function scrollActiveSentenceIntoView() {
  const activeCard = els.sentenceList.querySelector(".sentence-card.active");
  if (activeCard) {
    activeCard.scrollIntoView({ block: "center" });
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll('"', "&quot;");
}

function formatHistoryDate(value) {
  if (!value) {
    return "-";
  }
  const normalized = String(value).replace("T", " ");
  return normalized.slice(0, 16);
}

function renderHistoryList() {
  const items = state.currentHistoryItems.slice(0, 10);
  if (!items.length) {
    els.historyList.innerHTML = '<span class="history-empty">暂无历史翻译</span>';
    return;
  }

  els.historyList.innerHTML = items
    .map(
      (item) => `
        <button class="history-chip ${item.id === state.activeHistoryId ? "active" : ""}"
          data-history-id="${item.id}" type="button">
          ${formatHistoryDate(item.created_time || item.updated_time)}
        </button>
      `,
    )
    .join("");
}

function showHistoryItem(item) {
  state.activeHistoryId = item.id;
  state.lastReview = item;
  els.userTranslationInput.value = item.translation_content || "";
  els.scoreText.textContent = item.ai_score ?? "-";
  els.commentText.textContent = item.ai_comment || "等待点评";
  renderHistoryList();
}

function renderSentence() {
  const sentence = currentSentence();
  const hasSentence = Boolean(sentence);

  renderSourceText(sentence);
  els.sentencePosition.textContent = hasSentence
    ? `第 ${sentence.sentence_index} / ${state.sentenceTotal || state.sentences.length} 句`
    : state.selectedArticleId
      ? "请选择句子"
      : "未选择文章";

  els.createLlmButton.disabled = !hasSentence || state.isGeneratingLlm;
  els.createLlmButton.hidden = !hasSentence;
  els.submitReviewButton.disabled = !hasSentence || state.isSubmittingReview;

  state.llmTranslation = null;
  state.lastReview = null;
  state.currentHistoryItems = [];
  state.activeHistoryId = null;
  els.llmTranslationText.textContent = hasSentence ? "等待生成" : "等待选择句子";
  els.userTranslationInput.value = "";
  els.scoreText.textContent = "-";
  els.commentText.textContent = "等待点评";
  renderHistoryList();

  if (hasSentence) {
    loadSentenceTranslations(sentence.id).catch((error) => toast(error.message, "error"));
  }
}

async function loadArticles() {
  const data = await api("/articles?page=1&page_size=100");
  state.articles = data.items || [];
  if (!state.selectedArticleId && state.articles.length) {
    state.selectedArticleId = state.articles[0].id;
  }
  renderArticleSelect();
  if (state.selectedArticleId) {
    await resetAndLoadSentences(state.selectedArticleId, { locateLatest: true });
  } else {
    renderSentenceList();
    renderSentence();
  }
}

async function resetAndLoadSentences(articleId, options = {}) {
  state.selectedArticleId = Number(articleId);
  state.sentences = [];
  state.currentSentenceId = null;
  state.sentencePage = 1;
  state.firstSentencePage = 1;
  state.lastSentencePage = 0;
  state.sentenceTotal = 0;
  state.translationStatus = {};
  state.currentHistoryItems = [];
  state.activeHistoryId = null;
  els.sentenceList.scrollTop = 0;
  renderSentenceList({ preserveScroll: false });

  if (options.locateLatest) {
    const latest = await loadLatestUserTranslationSentence(state.selectedArticleId);
    if (latest?.sentence?.sentence_index) {
      await selectSentenceByIndex(latest.sentence.sentence_index);
      return;
    }
  }

  await loadSentencesPage("next", { refreshCurrent: true });
}

async function loadLatestUserTranslationSentence(articleId) {
  return api(
    `/user-sentence-translations/latest-sentence?article_id=${articleId}&user_id=${state.userId}`,
  );
}

async function fetchSentencesPage(page) {
  return api(
    `/article-sentences?article_id=${state.selectedArticleId}&page=${page}&page_size=${state.sentencePageSize}`,
  );
}

async function ensureSentenceContext(sentence) {
  if (!sentence || !state.selectedArticleId) {
    return;
  }

  const startIndex = Math.max(1, sentence.sentence_index - 5);
  const endIndex =
    state.sentenceTotal > 0
      ? Math.min(state.sentenceTotal, sentence.sentence_index + 5)
      : sentence.sentence_index + 5;
  const startPage = sentencePageForIndex(startIndex);
  const endPage = sentencePageForIndex(endIndex);
  const requests = [];

  for (let page = startPage; page <= endPage; page += 1) {
    const pageLoaded = state.sentences.some(
      (item) => sentencePageForIndex(item.sentence_index) === page,
    );
    if (!pageLoaded) {
      requests.push(fetchSentencesPage(page));
    }
  }

  if (!requests.length) {
    return;
  }

  const pages = await Promise.all(requests);
  const items = pages.flatMap((page) => page.items || []);
  const pageNumbers = pages.map((page) => page.page);
  state.sentenceTotal =
    pages.find((page) => page.total)?.total || state.sentenceTotal;
  mergeSentences(items);
  state.firstSentencePage = Math.min(state.firstSentencePage, ...pageNumbers);
  state.lastSentencePage = Math.max(state.lastSentencePage, ...pageNumbers);
  hydrateTranslationStatus(items).catch((error) => toast(error.message, "error"));
}

function totalSentencePages() {
  if (!state.sentenceTotal) {
    return 0;
  }
  return Math.ceil(state.sentenceTotal / state.sentencePageSize);
}

async function loadSentencesPage(direction = "next", options = {}) {
  if (!state.selectedArticleId || state.isLoadingSentences) {
    return;
  }

  const isPrevious = direction === "previous";
  const totalPages = totalSentencePages();
  const targetPage = isPrevious
    ? state.firstSentencePage - 1
    : state.lastSentencePage > 0
      ? state.lastSentencePage + 1
      : state.sentencePage;

  if (isPrevious && targetPage < 1) {
    return;
  }
  if (!isPrevious && totalPages > 0 && targetPage > totalPages) {
    return;
  }

  const previousScrollHeight = els.sentenceList.scrollHeight;
  const previousScrollTop = els.sentenceList.scrollTop;
  state.isLoadingSentences = true;
  renderSentenceList();
  try {
    const data = await fetchSentencesPage(targetPage);
    const items = data.items || [];
    state.sentenceTotal = data.total || 0;
    mergeSentences(items);
    state.firstSentencePage =
      state.firstSentencePage > 0
        ? Math.min(state.firstSentencePage, targetPage)
        : targetPage;
    state.lastSentencePage = Math.max(state.lastSentencePage, targetPage);
    state.sentencePage = state.lastSentencePage + 1;
    if (!state.currentSentenceId && state.sentences.length) {
      state.currentSentenceId = state.sentences[0].id;
    }
    hydrateTranslationStatus(items).catch((error) => toast(error.message, "error"));
  } finally {
    state.isLoadingSentences = false;
    renderSentenceList();
    if (isPrevious) {
      const heightDelta = els.sentenceList.scrollHeight - previousScrollHeight;
      els.sentenceList.scrollTop = previousScrollTop + heightDelta;
    }
    if (options.refreshCurrent) {
      renderSentence();
    }
  }
}

async function jumpToSentence() {
  if (!state.selectedArticleId) {
    toast("请先选择文章", "error");
    return;
  }

  const targetIndex = Number(els.jumpSentenceInput.value);
  if (!Number.isInteger(targetIndex) || targetIndex < 1) {
    toast("请输入有效句子编号", "error");
    return;
  }
  if (state.sentenceTotal > 0 && targetIndex > state.sentenceTotal) {
    toast(`句子编号不能超过 ${state.sentenceTotal}`, "error");
    return;
  }

  await selectSentenceByIndex(targetIndex);
}

async function selectSentenceByIndex(targetIndex) {
  const loadedSentence = state.sentences.find(
    (sentence) => sentence.sentence_index === targetIndex,
  );
  if (loadedSentence) {
    state.currentSentenceId = loadedSentence.id;
    await ensureSentenceContext(loadedSentence);
    renderSentenceList();
    updateActiveSentenceCard();
    scrollActiveSentenceIntoView();
    renderSentence();
    return;
  }

  const targetPage = Math.ceil(targetIndex / state.sentencePageSize);
  state.isLoadingSentences = true;
  renderSentenceList();
  try {
    const data = await fetchSentencesPage(targetPage);
    const items = data.items || [];
    state.sentenceTotal = data.total || state.sentenceTotal;
    state.sentences = items;
    state.sentencePage = targetPage + 1;
    state.firstSentencePage = targetPage;
    state.lastSentencePage = targetPage;

    const targetSentence = items.find(
      (sentence) => sentence.sentence_index === targetIndex,
    );
    if (!targetSentence) {
      return;
    }

    state.currentSentenceId = targetSentence.id;
    await ensureSentenceContext(targetSentence);
    hydrateTranslationStatus(items).catch((error) => toast(error.message, "error"));
  } finally {
    state.isLoadingSentences = false;
    renderSentenceList({ preserveScroll: false });
    scrollActiveSentenceIntoView();
    renderSentence();
  }
}

async function moveCurrentSentence(offset) {
  const sentence = currentSentence();
  if (!sentence) {
    return;
  }

  const targetIndex = sentence.sentence_index + offset;
  if (targetIndex < 1 || (state.sentenceTotal > 0 && targetIndex > state.sentenceTotal)) {
    return;
  }

  await selectSentenceByIndex(targetIndex);
}

async function hydrateTranslationStatus(sentences) {
  const results = await Promise.all(
    sentences.map(async (sentence) => {
      const data = await api(
        `/user-sentence-translations?sentence_id=${sentence.id}&page=1&page_size=1`,
      );
      return [sentence.id, Boolean(data.items?.length)];
    }),
  );

  results.forEach(([sentenceId, hasTranslation]) => {
    state.translationStatus[sentenceId] = hasTranslation;
  });
  renderSentenceList();
}

async function loadSentenceTranslations(sentenceId) {
  const [llmData, userData] = await Promise.all([
    api(`/llm-sentence-translations?sentence_id=${sentenceId}&page=1&page_size=1`),
    api(`/user-sentence-translations?sentence_id=${sentenceId}&page=1&page_size=10`),
  ]);

  const llmItem = llmData.items?.[0];
  if (llmItem && currentSentence()?.id === sentenceId) {
    state.llmTranslation = llmItem;
    els.llmTranslationText.textContent = llmItem.translation_content;
    els.createLlmButton.hidden = true;
  }

  const userItems = userData.items || [];
  if (currentSentence()?.id === sentenceId) {
    state.currentHistoryItems = userItems;
    state.translationStatus[sentenceId] = Boolean(userItems.length);
    renderSentenceList();
    renderHistoryList();
  }

  const userItem = userItems[0];
  if (userItem && currentSentence()?.id === sentenceId) {
    showHistoryItem(userItem);
  }
}

async function createLlmTranslation() {
  const sentence = currentSentence();
  if (
    !sentence ||
    state.isGeneratingLlm ||
    els.createLlmButton.hidden ||
    els.createLlmButton.disabled
  ) {
    return;
  }

  state.isGeneratingLlm = true;
  els.createLlmButton.disabled = true;
  els.createLlmButton.classList.add("loading");
  setCreateLlmButtonLabel(true);
  els.llmTranslationText.textContent = "生成中...";
  try {
    const result = await api("/translations/llm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sentence_id: sentence.id,
        target_language: "中文",
      }),
    });
    state.llmTranslation = result;
    els.llmTranslationText.textContent = result.translation_content;
    els.createLlmButton.hidden = true;
    toast("AI 翻译已生成");
  } finally {
    state.isGeneratingLlm = false;
    els.createLlmButton.classList.remove("loading");
    setCreateLlmButtonLabel(false);
    els.createLlmButton.disabled = !currentSentence();
  }
}

async function submitReview() {
  const sentence = currentSentence();
  const translation = els.userTranslationInput.value.trim();
  if (!sentence || !translation) {
    toast("请输入用户翻译", "error");
    return;
  }
  if (state.isSubmittingReview) {
    return;
  }

  state.isSubmittingReview = true;
  els.submitReviewButton.disabled = true;
  els.submitReviewButton.classList.add("loading");
  setSubmitReviewButtonLabel(true);
  els.commentText.textContent = "点评中...";
  try {
    const result = await api("/translations/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sentence_id: sentence.id,
        target_language: "中文",
        translation_content: translation,
        user_id: 0,
      }),
    });

    state.lastReview = result;
    state.translationStatus[sentence.id] = true;
    els.scoreText.textContent = result.ai_score ?? "-";
    els.commentText.textContent = result.ai_comment || "等待点评";
    renderSentenceList();
    await loadSentenceTranslations(sentence.id);
    toast("点评已完成");
  } finally {
    state.isSubmittingReview = false;
    els.submitReviewButton.classList.remove("loading");
    setSubmitReviewButtonLabel(false);
    els.submitReviewButton.disabled = !currentSentence();
  }
}

async function uploadArticle(event) {
  event.preventDefault();
  if (state.isUploadingArticle) {
    return;
  }

  const formData = new FormData(els.uploadForm);
  state.isUploadingArticle = true;
  els.uploadSubmitButton.disabled = true;
  els.uploadSubmitButton.classList.add("loading");
  els.uploadSubmitButton.textContent = "处理中";
  try {
    await api("/articles/upload-epub", {
      method: "POST",
      body: formData,
    });
    els.uploadDialog.close();
    els.uploadForm.reset();
    els.uploadForm.elements.language_type.value = "english";
    state.selectedArticleId = null;
    await loadArticles();
    toast("文章已添加");
  } finally {
    state.isUploadingArticle = false;
    els.uploadSubmitButton.classList.remove("loading");
    els.uploadSubmitButton.textContent = "上传并切句";
    els.uploadSubmitButton.disabled = false;
  }
}

function handleSentenceListScroll() {
  const nearTop = els.sentenceList.scrollTop <= 24;
  const nearBottom =
    els.sentenceList.scrollTop + els.sentenceList.clientHeight >=
    els.sentenceList.scrollHeight - 24;

  if (nearTop) {
    loadSentencesPage("previous").catch((error) => toast(error.message, "error"));
    return;
  }

  if (nearBottom) {
    loadSentencesPage("next").catch((error) => toast(error.message, "error"));
  }
}

function isTextEditingTarget(target) {
  if (!(target instanceof HTMLElement)) {
    return false;
  }
  return (
    target.isContentEditable ||
    ["INPUT", "SELECT", "TEXTAREA"].includes(target.tagName)
  );
}

function handleKeyboardShortcuts(event) {
  if (event.ctrlKey && event.key === "Enter") {
    event.preventDefault();
    if (event.shiftKey) {
      createLlmTranslation().catch((error) => toast(error.message, "error"));
    } else {
      submitReview().catch((error) => toast(error.message, "error"));
    }
    return;
  }

  if (
    event.ctrlKey ||
    event.metaKey ||
    event.altKey ||
    isTextEditingTarget(event.target)
  ) {
    return;
  }

  if (event.key === "ArrowUp") {
    event.preventDefault();
    moveCurrentSentence(-1).catch((error) => toast(error.message, "error"));
  }

  if (event.key === "ArrowDown") {
    event.preventDefault();
    moveCurrentSentence(1).catch((error) => toast(error.message, "error"));
  }
}

document.addEventListener("click", (event) => {
  const historyButton = event.target.closest("[data-history-id]");
  if (historyButton) {
    const item = state.currentHistoryItems.find(
      (historyItem) => historyItem.id === Number(historyButton.dataset.historyId),
    );
    if (item) {
      showHistoryItem(item);
    }
    return;
  }

  const sentenceButton = event.target.closest("[data-sentence-id]");
  if (!sentenceButton) {
    return;
  }
  state.currentSentenceId = Number(sentenceButton.dataset.sentenceId);
  updateActiveSentenceCard();
  const sentence = currentSentence();
  ensureSentenceContext(sentence)
    .then(() => {
      renderSentenceList();
      updateActiveSentenceCard();
      renderSentence();
    })
    .catch((error) => toast(error.message, "error"));
});

els.articleSelect.addEventListener("change", (event) => {
  resetAndLoadSentences(event.target.value, { locateLatest: true }).catch((error) =>
    toast(error.message, "error"),
  );
});

els.jumpSentenceForm.addEventListener("submit", (event) => {
  event.preventDefault();
  jumpToSentence().catch((error) => toast(error.message, "error"));
});

els.sentenceList.addEventListener("scroll", handleSentenceListScroll);
document.addEventListener("keydown", handleKeyboardShortcuts);

document.querySelector("#openUploadButton").addEventListener("click", () => {
  els.uploadDialog.showModal();
});

document.querySelector("#closeUploadButton").addEventListener("click", () => {
  els.uploadDialog.close();
});

els.createLlmButton.addEventListener("click", () => {
  createLlmTranslation().catch((error) => toast(error.message, "error"));
});
els.submitReviewButton.addEventListener("click", () => {
  submitReview().catch((error) => toast(error.message, "error"));
});
els.uploadForm.addEventListener("submit", (event) => {
  uploadArticle(event).catch((error) => toast(error.message, "error"));
});

loadArticles().catch((error) => toast(error.message, "error"));
