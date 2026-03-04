export default function Landing() {
  return (
    <div className="flex py-[204px] px-0 justify-center items-center bg-[#3B3B3B] min-w-screen min-h-screen overflow-hidden">
      <div className="shrink-0 w-[295px] h-[424px] relative">
        <button className="cursor-pointer text-nowrap flex p-[var(--sds-size-space-300)px] justify-center items-center gap-[var(--sds-size-space-200)] rounded-[var(--sds-size-radius-200)px] bg-[#FFF] shadow-[4px6px4px0rgba(0,0,0,0.25)] w-[248px] absolute left-6 top-[311px] overflow-hidden">
          <p className="text-[var(--sds-color-text-brand-default)] font-var(SdsTypographyBodyFontFamily) text-[var(--sds-typography-body-size-medium)] leading-none w-fit">
            Sign-in
          </p>
        </button>
        <div className="inline-flex items-start absolute left-6 top-96">
          <button className="cursor-pointer text-nowrap flex p-[var(--sds-size-space-300)px] justify-center items-center gap-[var(--sds-size-space-200)] rounded-[var(--sds-size-radius-200)px] bg-[#3CBC54] shadow-[4px6px4px0rgba(0,0,0,0.25)] w-[248px] absolute left-0 top-0 overflow-hidden">
            <p className="text-[var(--sds-color-text-brand-on-brand)] font-var(SdsTypographyBodyFontFamily) text-[var(--sds-typography-body-size-medium)] leading-none w-fit">
              Create Account
            </p>
          </button>
        </div>
        <svg
          width="295"
          height="295"
          viewBox="0 0 295 295"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="flex p-[37px] justify-center items-center w-[295px] h-[295px] absolute left-0 top-0 overflow-hidden "
        >
          <path
            d="M61.4583 258.125H233.542C247.119 258.125 258.125 247.119 258.125 233.542V61.4583C258.125 47.8813 247.119 36.875 233.542 36.875H61.4583C47.8813 36.875 36.875 47.8813 36.875 61.4583V233.542C36.875 247.119 47.8813 258.125 61.4583 258.125ZM61.4583 258.125L196.667 122.917L258.125 184.375M122.917 104.479C122.917 114.662 114.662 122.917 104.479 122.917C94.2964 122.917 86.0417 114.662 86.0417 104.479C86.0417 94.2964 94.2964 86.0417 104.479 86.0417C114.662 86.0417 122.917 94.2964 122.917 104.479Z"
            stroke="#B3B3B3"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    </div>
  );
}