def keygen(key: int):
    """
    TensorStore requires a GCP key set even if for a public dataset, so we'd need
    to sync up the gcp credentials to GitHub somehow. Instead of plain JSON file, we
    used an obfuscated file and reverse the obfuscation for the key.

    This is NOT a serious encryption - just a thin protection layer for a burner account credentials

    """
    with open('./hash.obs', 'rb') as f_in, open('gcp.json', 'wb') as f_out:
        data = f_in.read()
        f_out.write(bytes([b ^ key for b in data]))