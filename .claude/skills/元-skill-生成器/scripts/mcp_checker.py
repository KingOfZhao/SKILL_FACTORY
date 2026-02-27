def check_mcp_association(desc: str) -> bool:
    keywords = ["api", "database", "real-time", "github", "file system", "external", "live data"]
    return any(k in desc.lower() for k in keywords)