class Config:
    def __init__(self, max_token_count=1024 * 1023, max_buffer_size=2_048, max_token_size=512, enforce_schema=False, skip_invalid_nodes=False, skip_invalid_edges=False, separator=',', quoting=3, store_node_identifiers=False):
        """Settings for this run of the bulk loader"""
        # Maximum number of tokens per query
        # 1024 * 1024 is the hard-coded Redis maximum. We'll set a slightly lower limit so
        # that we can safely ignore tokens that aren't binary strings
        # ("GRAPH.BULK", "BEGIN", graph name, counts)
        self.max_token_count = min(max_token_count, 1024 * 1023)
        # Maximum size in bytes per query
        self.max_buffer_size = max_buffer_size * 1_000_000
        # Maximum size in bytes per token
        # 512 megabytes is a hard-coded Redis maximum
        self.max_token_size = min(max_token_size * 1_000_000, 512 * 1_000_000)

        self.enforce_schema = enforce_schema
        self.skip_invalid_nodes = skip_invalid_nodes
        self.skip_invalid_edges = skip_invalid_edges
        self.separator = separator
        self.quoting = quoting

        # True if we are building relations as well as nodes
        self.store_node_identifiers = store_node_identifiers
