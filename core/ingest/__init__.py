"""Zone A — ingest: the storage engine's write path (BUILD-SPEC §8, §9).

Parses the owner's Logseq vault into the immutable raw store (content-addressed, dedup),
extracts the explicit graph layer the owner authored (tags, [[links]]), and chunks notes
for embedding. Everything ingested here is provenance AUTHORED — the mirror's ground
truth. Embedding + LanceDB indexing build on these records (next increment).
"""
