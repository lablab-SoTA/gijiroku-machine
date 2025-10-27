import { render, screen } from "@testing-library/react";
import { SegmentList } from "../components/SegmentList";

describe("SegmentList", () => {
  it("renders speaker segments with formatted time", () => {
    render(
      <SegmentList
        segments={[
          { speaker: "Aさん", start: 0, end: 62, text: "おはようございます。" },
          { speaker: "Bさん", start: 62, end: 130, text: "議題に進みます。" }
        ]}
      />
    );

    expect(screen.getByText("Aさん")).toBeInTheDocument();
    expect(screen.getByText("1:02 - 2:10")).toBeInTheDocument();
    expect(screen.getByText("議題に進みます。")).toBeInTheDocument();
  });

  it("shows fallback when no segments are present", () => {
    render(<SegmentList segments={[]} />);

    expect(screen.getByText("セグメントが存在しません。")).toBeInTheDocument();
  });
});
