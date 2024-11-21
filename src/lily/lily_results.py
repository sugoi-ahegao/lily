from lily.models.stash_graphql_models.stash_plugin_config import StashPluginConfig


class Counter:
    def __init__(self):
        self._disabled_reason = None
        self._enabled = True
        self._count = 0

    def inc(self):
        if not self._enabled:
            raise RuntimeError(f"Counter is disabled: {self._disabled_reason}")

        self._count += 1

    def get_count(self):
        if not self._enabled:
            raise RuntimeError(f"Counter is disabled: {self._disabled_reason}")

        return self._count

    def disable(self, reason: str):
        self._enabled = False
        self._disabled_reason = reason

    def is_enabled(self):
        return self._enabled


class LilyResults:
    scenes_processed_counter: Counter
    videos_processed_counter: Counter
    filtered_out_counter: Counter
    path_unchanged_counter: Counter

    cross_drive_conflict_counter: Counter
    renamed_counter: Counter
    rename_failed_counter: Counter
    dry_run_renamed_counter: Counter

    @classmethod
    def setup(cls, config: StashPluginConfig):
        cls.scenes_processed_counter = Counter()
        cls.videos_processed_counter = Counter()
        cls.filtered_out_counter = Counter()
        cls.path_unchanged_counter = Counter()

        cls.cross_drive_conflict_counter = Counter()
        cls.renamed_counter = Counter()
        cls.rename_failed_counter = Counter()
        cls.dry_run_renamed_counter = Counter()

        if config.allow_rename_across_drives:
            cls.cross_drive_conflict_counter.disable("Renaming across drives is allowed")

        if config.dry_run_disabled:
            cls.dry_run_renamed_counter.disable("Dry-Run mode is disabled")

        if not config.dry_run_disabled:
            cls.renamed_counter.disable("Dry-Run mode is enabled")
            cls.rename_failed_counter.disable("Dry-Run mode is enabled, no rename failures possible")

    @classmethod
    def get_results(cls):
        if cls.dry_run_renamed_counter.is_enabled():
            return f"Summary: [DRY-RUN] {cls.dry_run_renamed_counter.get_count()} video(s) would be renamed."

        return f"Summary: {cls.renamed_counter.get_count()} video(s) renamed."

    @classmethod
    def get_detailed_results(cls):
        def format_count_if_enabled(counter: Counter, append: str = "") -> str:
            if counter.is_enabled():
                return f"{counter.get_count()} {append}"
            else:
                return ""

        results: list[str] = []

        results.append(
            f"{cls.videos_processed_counter.get_count()} video(s) processed"
            + f" ({cls.scenes_processed_counter.get_count()} scene(s))"
        )
        results.append(f"{cls.filtered_out_counter.get_count()} filtered out")
        results.append(f"{cls.path_unchanged_counter.get_count()} path(s) unchanged")
        results.append(format_count_if_enabled(cls.cross_drive_conflict_counter, "cross drive conflict(s)"))
        results.append(format_count_if_enabled(cls.dry_run_renamed_counter, "would be renamed"))
        results.append(format_count_if_enabled(cls.rename_failed_counter, "rename(s) failed"))
        results.append(format_count_if_enabled(cls.renamed_counter, "renamed"))

        # filter out empty results
        results = [result for result in results if result != ""]

        return "Detailed Summary: " + " -> ".join(results)
