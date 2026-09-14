# Historical: Mongi Renderer V1.6.9 — Soft Organic Bubble Patch

> 보관용 이전 패치 기록이다. 현재 Renderer V1.7.0 / Edit Lock V1.9에서는 dialogue/thought Renderer 합성이 폐기되었다.

Apply over the working V1.6.8 Renderer root.

Changes:
- `dialogue` / `thought`: replaces dark outlined rounded rectangles with deterministic irregular cloud-like bubbles.
- No dark outline; warm semi-transparent ivory/white fill; softly feathered edge.
- `thought` receives a slightly airier silhouette.
- Other text roles are unchanged.
- TYPEWRITER remains compatible because bubble dimensions are fixed before progressive text rendering.
- Cache schema bumped so old geometric bubble cut caches are not reused.
- Bundles Edit Lock V1.7.2 documenting the official bubble rule.

No audio/BGM/font assets are included or modified.
