class ParamSet:
    """A class for holding and validating the GET params

    It validates the most of params with their restrictions. And also validate the required values for each mode
    """
    AVAILABLE_MODES = (
        'thumbnail', 'resize', 'flip', 'rotate',
    )

    AVAILABLE_FORMATS = (
        'jpg', 'jpeg', 'png',
    )

    VALID_HORIZONTAL_DIRECTIONS = (
        'h', 'horizontal',
    )

    VALID_VERTICAL_DIRECTIONS = (
        'v', 'vertical',
    )

    VALID_TRUE_BOOL_STRINGS = (
        'true', 't', '1', 'yes',
    )

    VALID_FALSE_BOOL_STRINGS = (
        'false', 'f', '0', 'no',
    )

    def __init__(self, mode=None, path=None, img_format='png', width=None, height=None,
                 upscale='true', quality='100', direction=None, degree=None):
        """Initialize the parameters for fitter server

        TODO: Supports external URL of an image as 'url' field

        :param mode: The operation mode. One of followings
            - thumbnail
            - resize
            - flip
            - rotate
        :param path: The path of image which is on source storage
        :param img_format: The desired format of image
            - png
            - jpg
            - jpeg
        :param width: The desired width of image. If this value is 0, the aspect ratio of output image is preserved
        :param height: The desired height of image. If this value is 0, the aspect ratio of output image is preserved
        :param upscale: Whether if upscale the image has size smaller than desired size
        :param quality: The desired quality of image
        :param direction: The desired direction to flip the image
        :param degree: The desired degree to rotate the image
        :return: None. But will set all params to itself
        """

        # For operation. One of followings
        self.mode = mode

        # For image url or path on source storage
        self.path = path

        # For operation conditions
        self.width = width
        self.height = height
        self.direction = direction
        self.degree = degree
        self.img_format = img_format
        self.upscale = upscale
        self.quality = quality
        self.options = {
            'format': self.img_format,
            'upscale': self.upscale,
            'quality': self.quality,
        }
        self.errors = []

    def _validate_mode(self):
        if self.mode is None:
            self.errors.append('You must specify the \'mode\'')
            return False
        if self.mode not in self.AVAILABLE_MODES:
            self.errors.append('The \'mode\' must be one of {}'.format(self.AVAILABLE_MODES))
            return False
        return True

    def _validate_path(self):
        if self.path is None:
            self.errors.append('You must specify the \'path\' of an image')
            return False
        return True

    def _validate_foramt(self):
        if self.options['format'] not in self.AVAILABLE_FORMATS:
            self.errors.append('The \'format\' must be one of {}'.format(self.AVAILABLE_FORMATS))
            return False
        return True

    def _validate_width(self):
        if self.width is not None:
            if not self.width.isnumeric():
                self.errors.append('Only numeric value is allowed for \'width\'')
                return False
            self.width = int(self.width)
            if self.width < 0:
                self.errors.append('The \'width\' can not be negative')
                return False
        return True

    def _validate_height(self):
        if self.height is not None:
            if not self.height.isnumeric():
                self.errors.append('Only numeric value is allowed for \'height\'')
                return False
            self.height = int(self.height)
            if self.height < 0:
                self.errors.append('The \'height\' can not be negative')
                return False
        return True

    def _validate_upscale(self):
        if self.options['upscale'] in self.VALID_TRUE_BOOL_STRINGS:
            self.options['upscale'] = True
            return True
        if self.options['upscale'] in self.VALID_FALSE_BOOL_STRINGS:
            self.options['upscale'] = False
            return True
        self.errors.append('Only bool string is allowed for \'upscale\': {}'.format(
            self.VALID_TRUE_BOOL_STRINGS + self.VALID_FALSE_BOOL_STRINGS))
        return False

    def _validate_quality(self):
        if not self.options['quality'].isnumeric():
            self.errors.append('Only numeric value is allowed for \'quality\'')
            return False
        self.options['quality'] = int(self.options['quality'])
        if self.options['quality'] <= 0 or self.options['quality'] > 100:
            self.errors.append('The quality must be in between 1 and 100')
            return False
        return True

    def _validate_direction(self):
        if self.direction is not None:
            if self.direction in self.VALID_HORIZONTAL_DIRECTIONS:
                self.direction = 'h'
                return True
            if self.direction in self.VALID_VERTICAL_DIRECTIONS:
                self.direction = 'v'
                return True
            self.errors.append(
                'The \'direction\' must be one of {}'.format(
                    self.VALID_HORIZONTAL_DIRECTIONS + self.VALID_VERTICAL_DIRECTIONS))
            return False
        return True

    def _validate_degree(self):
        if self.degree is not None:
            if not self.degree.isnumeric():
                self.errors.append('Only numeric value is allowed for \'degree\'')
                return False
            self.degree = float(self.degree)
            return True
        return True

    def _validate_required_for_resizing(self):
        if self.width is None and self.height is None:
            self.errors.append('At least one of \'width\' or \'height\' have to be set')
            return False
        if self.width == 0 and self.height == 0:
            self.errors.append('At least one of \'width\' or \'height\' have to be positive')
            return False
        return True

    def _validate_required_for_flipping(self):
        if self.direction is None:
            self.errors.append('The \'direction\' have to be set to flip the image')
            return False
        return True

    def _validate_required_for_rotating(self):
        if self.degree is None:
            self.errors.append('The \'degree\' have to be set to rotate the image')
            return False
        return True

    def validate(self):
        """Validate the restrictions of params and conditions of mode

         :return: True if all validation is passed, False otherwise
        """
        # TODO: Validate the only required parameters for each mode
        basic_validated = all([self._validate_mode(),
                               self._validate_path(),
                               self._validate_foramt(),
                               self._validate_width(),
                               self._validate_height(),
                               self._validate_upscale(),
                               self._validate_quality(),
                               self._validate_direction(),
                               self._validate_degree()])
        if not basic_validated:
            return basic_validated
        # Validate the required conditions for each mode
        if self.mode == 'thumbnail' or self.mode == 'resize':
            return self._validate_required_for_resizing()
        if self.mode == 'flip':
            return self._validate_required_for_flipping()
        if self.mode == 'rotate':
            return self._validate_required_for_rotating()
