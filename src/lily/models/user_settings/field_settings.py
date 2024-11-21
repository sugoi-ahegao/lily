from lily.fields.date_field import DateFieldSettings
from lily.fields.performers_field import PerformerFieldSettings
from lily.fields.rating_field import RatingFieldSettings
from lily.fields.resolution_field import ResolutionFieldSettings
from lily.fields.studio_field import StudioFieldSettings
from lily.fields.studio_hierarchy_as_path_field import StudioHierarchyAsPathFieldSettings
from lily.fields.studio_hierarchy_field import StudioHierarchyFieldSettings
from lily.fields.title_field import TitleFieldSettings
from lily.fields.watched_field import WatchedFieldSettings
from lily.models.core import BaseModelWithExactAttributes


class FieldSettings(BaseModelWithExactAttributes):
    date: DateFieldSettings = DateFieldSettings()
    performers: PerformerFieldSettings = PerformerFieldSettings()
    rating: RatingFieldSettings = RatingFieldSettings()
    resolution: ResolutionFieldSettings = ResolutionFieldSettings()
    studio: StudioFieldSettings = StudioFieldSettings()
    studio_hierarchy_as_path: StudioHierarchyAsPathFieldSettings = StudioHierarchyAsPathFieldSettings()
    studio_hierarchy: StudioHierarchyFieldSettings = StudioHierarchyFieldSettings()
    title: TitleFieldSettings = TitleFieldSettings()
    watched: WatchedFieldSettings = WatchedFieldSettings()
